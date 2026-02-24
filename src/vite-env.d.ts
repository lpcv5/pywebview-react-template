/// <reference types="vite/client" />

interface PyWebViewApi {
  greet(name: string): Promise<string>;
}

interface Window {
  pywebview: {
    api: PyWebViewApi;
  };
}

interface WindowEventMap {
  pywebviewready: Event;
}
