const fs = require('fs');

// Read Firebase configuration from Vercel's environment variables
const configJson = process.env.FIREBASE_CONFIG || '{}';

// Build the keys.js content
const content = `export const firebaseConfig = ${configJson};\n`;

// Write the file so Vercel can serve it statically
try {
  fs.writeFileSync('./keys.js', content);
  console.log('keys.js generated successfully.');
} catch (err) {
  console.error('Error generating keys.js:', err);
  process.exit(1);
}
