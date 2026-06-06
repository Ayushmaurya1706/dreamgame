const fs = require('fs');

// Read individual Firebase environment variables
const firebaseConfig = {
  apiKey: process.env.apiKey || process.env.API_KEY || '',
  authDomain: process.env.authDomain || process.env.AUTH_DOMAIN || '',
  projectId: process.env.projectId || process.env.PROJECT_ID || '',
  storageBucket: process.env.storageBucket || process.env.STORAGE_BUCKET || '',
  messagingSenderId: process.env.messagingSenderId || process.env.MESSAGING_SENDER_ID || '',
  appId: process.env.appId || process.env.APP_ID || '',
  measurementId: process.env.measurementId || process.env.MEASUREMENT_ID || ''
};

console.log('--- Firebase Key Generation Debug ---');
console.log('apiKey present:', !!firebaseConfig.apiKey);
console.log('authDomain present:', !!firebaseConfig.authDomain);
console.log('projectId present:', !!firebaseConfig.projectId);
console.log('-------------------------------------');

// Build the keys.js content
const content = `export const firebaseConfig = ${JSON.stringify(firebaseConfig, null, 2)};\n`;

// Write the file so Vercel can serve it statically
try {
  fs.writeFileSync('./keys.js', content);
  console.log('keys.js file created successfully.');
} catch (err) {
  console.error('Error writing keys.js:', err);
  process.exit(1);
}
