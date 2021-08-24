## OCR Captcha Solver

The original motivation for this project was to create a neural network based service which can solve poorly designed captchas.  As a control, I implemented a simple OCR based service using <a href="https://pypi.org/project/pytesseract/">pytesseract</a>.  I built a browser automation script using <a href="https://github.com/puppeteer/puppeteer">puppeteer</a>, to build a database of captchas.  Approximately 1008 captcha images were scraped and bifurcated into two folders:

<table>
<tbody>
  <tr><td colspan=2>Captchas</td></tr>
  <tr><td >Directory Name</td><td># Files</td></tr>
  <tr><td >labled</td><td>386</td></tr>
  <tr><td >Unlabeled</td><td>622</td></tr>
</tbody>
</table>

Some examples of the data:
<table>
  <tbody>
    <tr><td>1ay4df</td><td>3ce2px</td></tr>
    <tr>
    <td>
      <img src="https://github.com/nps6-uwf/CaptchaBypass/blob/main/OCR%20Captcha%20Solver/figures/1ay4df.png?raw=true"></img>
    </td>
    <td>
      <img src="https://github.com/nps6-uwf/CaptchaBypass/blob/main/OCR%20Captcha%20Solver/figures/3ce2px.png?raw=true"></img>
    </td>
    </tr>
  </tbody>
</table>

With my labeled data, I attempted to read the captchas via OCR.  I developed a set of image preprocessing techniques, see <i>im_utils.py</i>.  Then I found the optimal set of preprocessing techniques by enumerating every combination, and then finding the set the produced the result text with the smallest Levenshtein distance from the correct label.  Next, I used the optimal preprocessing and focussed on the relationship between the OCR confidence and the actual accuracy of the result
