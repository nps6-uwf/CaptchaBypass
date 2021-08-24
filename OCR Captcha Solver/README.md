# OCR Captcha Solver

## Overview

The original motivation for this project was to create a neural network based service which can solve poorly designed captchas.  As a control, I implemented a simple OCR based service using <a href="https://pypi.org/project/pytesseract/">pytesseract</a>.  I built a browser automation script using <a href="https://github.com/puppeteer/puppeteer">puppeteer</a>, to build a database of captchas.  Approximately 1008 captcha images were scraped and bifurcated into two folders:

<table>
<tbody>
  <tr><td colspan=2>Captchas</td></tr>
  <tr><td >Directory Name</td><td># Files</td></tr>
  <tr><td >labled</td><td>386</td></tr>
  <tr><td >Unlabeled</td><td>622</td></tr>
</tbody>
</table>

Some examples of the data, notice how all of these sequences have 6 characters:
<table>
  <tbody>
    <tr><td>1AY4DF</td><td>3CE2PX</td><td>HEAZ76</td></tr>
    <tr>
    <td>
      <img src="https://github.com/nps6-uwf/CaptchaBypass/blob/main/OCR%20Captcha%20Solver/figures/1ay4df.png?raw=true"></img>
    </td>
    <td>
      <img src="https://github.com/nps6-uwf/CaptchaBypass/blob/main/OCR%20Captcha%20Solver/figures/3ce2px.png?raw=true"></img>
    </td>
    <td>
      <img src="https://github.com/nps6-uwf/CaptchaBypass/blob/main/OCR%20Captcha%20Solver/figures/heaz76.png?raw=true"></img>
    </td>
    </tr>
  </tbody>
</table>

With my labeled data, I attempted to read the captchas via OCR.  I developed a set of image preprocessing techniques, see <i>im_utils.py</i>.  Then I found the optimal set of preprocessing techniques by enumerating every combination, and then finding the set the produced the result text with the smallest Levenshtein distance from the correct label.  Next, I used the optimal preprocessing and focussed on the relationship between the OCR confidence and the actual accuracy of the result.  I also generated plots depicting the distribution of characters that were either correctly or incorrectly interpreted and a pie chart showing the proportion of result lengths that were correct:

<table>
  <tbody>
    <tr>
    <td><img src="https://github.com/nps6-uwf/CaptchaBypass/blob/main/OCR%20Captcha%20Solver/figures/correctCharacterDistribution.PNG?raw=true"></img></td>
    <td><img src="https://github.com/nps6-uwf/CaptchaBypass/blob/main/OCR%20Captcha%20Solver/figures/lengthDistribution.PNG?raw=true"></img></td>
    </tr>
  </tbody>
</table>

## Usage

<ol>
<li>
  <i>captchaService.py</i> implements findings from <i>main.py</i> to create a captcha solver api service.  The service uses Python's <a href="https://flask.palletsprojects.com/en/2.0.x/">Flask</a> module to create a server with a single route: <i>http://127.0.0.1:5000/{fname}/{threshold}/{rmFile}</i>.  The <i>test/req.py</i> file shows an example of how to make a request to the service.  
  </li>
</ol>
