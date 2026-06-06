const fs = require('fs');

// Read Firebase configuration from Vercel's environment variables
const configJson = process.env.FIREBASE_CONFIG;

console.log('--- Firebase Key Generation Debug ---');
if (!configJson) {
  console.warn('WARNING: FIREBASE_CONFIG environment variable is not defined or is empty!');
} else {
  console.log('FIREBASE_CONFIG found. Length:', configJson.length);
  try {
    JSON.parse(configJson);
    console.log('FIREBASE_CONFIG JSON syntax is valid.');
  } catch (parseErr) {
    console.error('ERROR: FIREBASE_CONFIG contains invalid JSON syntax!', parseErr.message);
  }
}
console.log('-------------------------------------');

// Build the keys.js content
const content = `export const firebaseConfig = ${configJson || '{}'};\n`;

// Write the file so Vercel can serve it statically
try {
  fs.writeFileSync('./keys.js', content);
  console.log('keys.js file created successfully.');
} catch (err) {
  console.error('Error writing keys.js:', err);
  process.exit(1);
}
