import { betterAuth } from 'better-auth'
import { emailOTP } from 'better-auth/plugins'
import { Pool } from 'pg'

type OtpType = 'sign-in' | 'email-verification' | 'forget-password'

type SendOtpArgs = {
  email: string
  otp: string
  type: OtpType
}

const databaseUrl = process.env.DATABASE_URL

if (!databaseUrl) {
  throw new Error('DATABASE_URL is required for Better Auth')
}

const pool = new Pool({ connectionString: databaseUrl })

const baseUrl = process.env.BETTER_AUTH_URL
const trustedOrigins = (process.env.BETTER_AUTH_TRUSTED_ORIGINS || process.env.FRONTEND_BASE_URL || 'http://localhost:3000')
  .split(',')
  .map(origin => origin.trim())
  .filter(Boolean)

const resendApiKey = process.env.RESEND_API_KEY
const resendFrom = process.env.RESEND_FROM
const googleClientId = process.env.GOOGLE_CLIENT_ID
const googleClientSecret = process.env.GOOGLE_CLIENT_SECRET

if (!googleClientId || !googleClientSecret) {
  throw new Error('GOOGLE_CLIENT_ID and GOOGLE_CLIENT_SECRET are required for Better Auth')
}

const subjectByType: Record<OtpType, string> = {
  'sign-in': 'Your EXQ Links login code',
  'email-verification': 'Verify your EXQ Links email',
  'forget-password': 'Reset your EXQ Links password'
}

async function sendOtpEmail({ email, otp, type }: SendOtpArgs) {
  if (!resendApiKey || !resendFrom) {
    if (process.env.NODE_ENV === 'production') {
      throw new Error('Resend is not configured. Set RESEND_API_KEY and RESEND_FROM to enable OTP email delivery.')
    }
    console.warn(`Resend is not configured. OTP for ${email}: ${otp}`)
    return
  }

  const subject = subjectByType[type] ?? 'Your EXQ Links verification code'
  const text = `Your EXQ Links verification code is ${otp}. It expires in 5 minutes.`
  const html = `
    <div style="font-family: ui-sans-serif, system-ui, -apple-system, sans-serif; line-height: 1.5;">
      <h2 style="margin: 0 0 12px;">Your verification code</h2>
      <p style="margin: 0 0 16px;">Use this one-time code to finish signing in:</p>
      <p style="font-size: 24px; font-weight: 600; letter-spacing: 2px; margin: 0 0 16px;">${otp}</p>
      <p style="margin: 0; color: #6b7280;">This code expires in 5 minutes.</p>
    </div>
  `.trim()

  const response = await fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: {
      'Authorization': `Bearer ${resendApiKey}`,
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      from: resendFrom,
      to: [email],
      subject,
      text,
      html
    })
  })

  if (!response.ok) {
    const errorText = await response.text()
    console.error(`Failed to send OTP email (${response.status}): ${errorText}`)
  }
}

export const auth = betterAuth({
  appName: 'EXQ Links',
  baseURL: baseUrl,
  trustedOrigins,
  database: pool,
  account: {
    accountLinking: {
      enabled: true,
      trustedProviders: ['google']
    }
  },
  socialProviders: {
    google: {
      clientId: googleClientId,
      clientSecret: googleClientSecret,
      scope: ['email', 'profile']
    }
  },
  plugins: [
    emailOTP({
      async sendVerificationOTP({ email, otp, type }) {
        await sendOtpEmail({ email, otp, type })
      }
    })
  ]
})
