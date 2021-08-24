## OCR Captcha Solver

The original motivation for this project was to create a neural network based service which can solve poorly designed captchas.  As a control, I implemented a simple OCR based service using <a href="https://pypi.org/project/pytesseract/">pytesseract</a>.  I built a browser automation script using <a href="https://github.com/puppeteer/puppeteer">puppeteer</a>, to build a database of captchas.  Approximately 1008 captcha images were scraped and bifurcated into two folders:

<table>
<tbody>
  <tr><td colspan=2>Captchas</td></tr>
  <tr><td >Directory Name</td><td># Files</td></tr>
  <tr><td >labled</td><td>326</td></tr>
  <tr><td >Unlabeled</td><td>644</td></tr>
</tbody>
</table>
