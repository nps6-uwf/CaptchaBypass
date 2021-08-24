// Author: NS
// Date: 8/20/2021
// Version 1:


const puppeteer = require('puppeteer');
const fs = require('fs');
const request = require('request');

const URL = ''; // website available on request.


const download = (uri, filename) => {
  /* Download a file (image) from uri. */
  return new Promise((resolve, reject) => {
    request.head(uri, function (err, res, body) {
      request(uri).pipe(fs.createWriteStream(filename)).on('close', resolve);
    });
  });
};


(async () => {
    const browser = await puppeteer.launch({headless: true});
    const page = await browser.newPage();
    await page.goto(URL,  {"waitUntil" : "networkidle0"});
    // selector: "a[onclick='zsRegenerateCaptcha()']"
    // captch image id: zsCaptchaUrl

    await page.waitForSelector("a[onclick='zsRegenerateCaptcha()']") 
    // page.waitForSelector("a[onclick='zsRegenerateCaptcha()']", {visible: true})
    .then(()=> console.log("Success A."))
    .catch((e)=> console.log("unexpected error A.", e));

    for(let i = 0; i < 101; ++i) {
      await page.click("a[onclick='zsRegenerateCaptcha()']");

      const imageUrl = await page.evaluate(
          // here we got the image url from the selector.
          () => document.querySelector('img#zsCaptchaUrl').src
      );
      console.log("image url: ", imageUrl);
      await download(imageUrl, `../captchas/image_${i}.png`);
      
    }
    await browser.close();
})();
