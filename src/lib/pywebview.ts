export function getPyWebViewApi(): Promise<PyWebViewApi> {
  if (window.pywebview?.api) {
    return Promise.resolve(window.pywebview.api);
  }

  return new Promise((resolve, reject) => {
    const timeout = setTimeout(() => {
      reject(new Error("pywebview API not available (timed out after 5s)"));
    }, 5000);

    window.addEventListener("pywebviewready", () => {
      clearTimeout(timeout);
      resolve(window.pywebview.api);
    }, { once: true });
  });
}
