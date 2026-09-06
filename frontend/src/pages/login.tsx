import { useState } from 'react'
import type { FormEvent } from 'react'
import { useLocation, useNavigate } from 'react-router-dom'

import { login } from '../services/api'

function Login() {
	const navigate = useNavigate()
	const location = useLocation()
	const [email, setEmail] = useState('')
	const [password, setPassword] = useState('')
	const [error, setError] = useState('')
	const [isSubmitting, setIsSubmitting] = useState(false)

	async function handleSubmit(event: FormEvent<HTMLFormElement>) {
		event.preventDefault()
		setError('')
		setIsSubmitting(true)

		try {
			const response = await login(email, password)
			localStorage.setItem('access_token', response.access_token)
			localStorage.setItem('current_user', JSON.stringify(response.user))
			const destination = (location.state as { from?: string } | null)?.from
			navigate(destination || '/dashboard', { replace: true })
		} catch {
			setError('Unable to sign in with those credentials.')
		} finally {
			setIsSubmitting(false)
		}
	}

	return (
		<main className="login-page">
			<section className="login-panel">
				<p className="eyebrow">Portfolio analytics</p>
				<h1>Welcome back</h1>
				<p className="login-copy">Sign in to review your portfolios and risk.</p>

				<form onSubmit={handleSubmit} className="login-form">
					<label>
						Email
						<input
							type="email"
							value={email}
							onChange={(event) => setEmail(event.target.value)}
							autoComplete="email"
							required
						/>
					</label>
					<label>
						Password
						<input
							type="password"
							value={password}
							onChange={(event) => setPassword(event.target.value)}
							autoComplete="current-password"
							required
						/>
					</label>
					{error && <p className="login-error">{error}</p>}
					<button type="submit" disabled={isSubmitting}>
						{isSubmitting ? 'Signing in...' : 'Sign in'}
					</button>
				</form>
			</section>
		</main>
	)
}

export default Login
