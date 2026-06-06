import { initializeApp } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-app.js";
import { getAuth } from "https://www.gstatic.com/firebasejs/10.8.0/firebase-auth.js";

// Attempt to load the untracked keys.js configuration
let config;
try {
  const keys = await import("./keys.js");
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
