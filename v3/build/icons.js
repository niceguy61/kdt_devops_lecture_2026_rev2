// lucide 아이콘을 SVG 파일로 내보낸다 (stroke=currentColor)
const React = require('react'); const RDS = require('react-dom/server');
const lu = require('react-icons/lu'); const fs = require('fs');
const names = process.argv.slice(2);
const want = names.length ? names : Object.keys(lu);
let miss = [];
for (const n of want) {
  const C = lu[n]; if (!C) { miss.push(n); continue; }
  const svg = RDS.renderToStaticMarkup(React.createElement(C, { size: 24 }));
  fs.writeFileSync(`icons/${n}.svg`, svg);
}
if (miss.length) console.log('missing:', miss.join(' '));
console.log('total lucide:', Object.keys(lu).length);
