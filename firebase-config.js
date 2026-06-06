import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";

// Attempt to load the untracked keys.js configuration
let config;
try {
  // Use a query parameter cache-buster to prevent the browser from caching old 404 errors
  const keys = await import("./keys.js?t=" + Date.now());
  config = keys.firebaseConfig;
} catch (error) {
  console.warn("Local keys.js not found. Using placeholder configuration.");
  config = {
    apiKey: "PLACEHOLDER_API_KEY",
    authDomain: "placeholder-auth-domain",
    projectId: "placeholder-project-id"
  };
}

const app = initializeApp(config);
const auth = getAuth(app);

export { auth };
