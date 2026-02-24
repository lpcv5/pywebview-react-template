import { useState } from "react";
import { Button } from "@/components/ui/button";
import { getPyWebViewApi } from "@/lib/pywebview";

function App() {
  const [response, setResponse] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);

  async function handleGreet() {
    setLoading(true);
    setError(null);
    try {
      const api = await getPyWebViewApi();
      const result = await api.greet("World");
      setResponse(result);
    } catch (e) {
      setError(e instanceof Error ? e.message : String(e));
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="flex min-h-screen items-center justify-center">
      <div className="flex flex-col items-center gap-6 p-8">
        <h1 className="text-3xl font-bold tracking-tight">
          pywebview + React
        </h1>
        <p className="text-muted-foreground">
          Click the button to call Python from JavaScript.
        </p>
        <Button onClick={handleGreet} disabled={loading} size="lg">
          {loading ? "Calling Python..." : "Greet from Python"}
        </Button>
        {response && (
          <p className="rounded-md bg-muted px-4 py-2 text-sm">{response}</p>
        )}
        {error && (
          <p className="rounded-md bg-destructive/10 px-4 py-2 text-sm text-destructive">
            {error}
          </p>
        )}
      </div>
    </div>
  );
}

export default App;
