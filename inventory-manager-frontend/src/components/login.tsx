import { type SyntheticEvent, useState } from "react";
import { LoginService } from "../services/login-service";

export function Login() {

  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (event: SyntheticEvent<HTMLFormElement>) => {
    event.preventDefault();
    const result: boolean = await LoginService.login(username, password);

    if (result) {
      // Handle successful login
    } else {
      // Handle login failure
    }
  }

  return (
    <div className="login">
      <div className="container">

        <div className="card">
          <h2 className="title">Login</h2>
          <form onSubmit={handleSubmit} className="form">
            <div className="input-group">
              <label htmlFor="username" className="label">Username</label>
              <input
                type="username"
                id="username"
                name="username"
                placeholder="Enter your username"
                value={username}
                onChange={(e) => setUsername(e.target.value)}
                required
                className="input"
              />
            </div>
            <div className="input-group">
              <label htmlFor="password" className="label">Password</label>
              <input
                type="password"
                id="password"
                name="password"
                placeholder="Enter your password"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                required
                className="input"
              />
            </div>
            <button type="submit" className="button">Login</button>
          </form>
        </div>
      </div>
    </div>)
}
