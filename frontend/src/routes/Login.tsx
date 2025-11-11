import { FormEvent, useState } from "react";
import { useAuth } from "../hooks/useAuth";
import { Button } from "../components/ui/Button";
import { TextField } from "../components/ui/TextField";

export const Login = () => {
  const { login, isAuthenticated } = useAuth();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [status, setStatus] = useState<string | null>(null);

  const handleSubmit = async (event: FormEvent<HTMLFormElement>) => {
    event.preventDefault();
    try {
      await login({ email, password });
      setStatus("Connexion réussie");
    } catch (error) {
      console.error(error);
      setStatus("Échec de la connexion");
    }
  };

  return (
    <div className="login-page">
      <h1>Accès Planner</h1>
      {isAuthenticated && <p data-testid="login-success">Session active</p>}
      <form onSubmit={handleSubmit}>
        <TextField label="Email" name="email" value={email} onChange={setEmail} type="email" required />
        <TextField
          label="Mot de passe"
          name="password"
          value={password}
          onChange={setPassword}
          type="password"
          required
        />
        <Button type="submit">Se connecter</Button>
      </form>
      {status && <p role="status">{status}</p>}
    </div>
  );
};

export default Login;
