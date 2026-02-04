
<h1 align="center">
  <br>
  <a href="https://www.narit.or.th"><img src="https://www.narit.or.th/_next/image?url=https%3A%2F%2Fweb-cms-service.narit.or.th%2Fassets%2F60b990f7-e977-4976-83c7-35820a3b826c&w=2048&q=75" alt="NARIT" width="200"></a>
  <br>
  Satellite ML
  <br>
</h1>

<h4 align="center">A machine learning toolkit for predicting satellite Two-Line Element (TLE) orbital data.</h4>

<!--<a href="http://electron.atom.io" target="_blank">Electron</a> -->
<p align="center">
  <a href="#key-features">Key Features</a> •
  <a href="#how-to-use">How To Use</a> •
  <a href="#support">Support</a> •

</p>

<!-- ![screenshot](https://raw.githubusercontent.com/amitmerchant1990/electron-markdownify/master/app/img/markdownify.gif) -->

## Key Features

* **SpaceTrack Data Retrieval**
  - Download historical TLE records from [SpaceTrack](https://www.space-track.org/auth/login), a publicly available satellite tracking database.

* **Model Training Pipelines**
  - Train and evaluate multiple ML approaches including Classical ML (Ridge Regression, Random Forest), LSTM neural networks, and ARIMA time-series models for TLE prediction.

* **Pretrained Models for Quick Inference**
  - Use ready-to-go Random Forest and LSTM models pretrained on ISS (International Space Station) TLE data for immediate predictions without training.

* **End-to-End Prediction Pipeline**
  - Predict future orbital parameters for any satellite by training models on each TLE feature (inclination, eccentricity, mean motion, etc.).
 
### Quick Start: Inference with Pretrained Models
If you want to make predictions using our pretrained models, follow the notebooks:
- `Inference_ClassicalML.ipynb` — Uses pretrained Random Forest models
- `Inference_pretrainedLSTM.ipynb` — Uses pretrained LSTM neural network

### Training Your Own Models
To train models on your own satellite data, explore the notebooks in the `Model_training/` directory.
<!-- * GitHub Flavored Markdown  
* Syntax highlighting
* [KaTeX](https://khan.github.io/KaTeX/) Support
* Dark/Light mode
* Toolbar for basic Markdown formatting
* Supports multiple cursors
* Save the Markdown preview as PDF
* Emoji support in preview :tada:
* App will keep alive in tray for quick usage
* Full screen mode
  - Write distraction free.
* Cross platform
  - Windows, macOS and Linux ready. -->

## How To Use

### Installation

We recommend creating a new Python environment to avoid dependency conflicts:

```bash
# Clone this repository
$ git clone https://github.com/Noppachanin/Narit-SATML
$ cd Narit-SATML

# (Optional) Create and activate a virtual environment
$ python -m venv venv
$ source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
$ pip install -r requirements.txt
```

### Notebook Descriptions

| Notebook | Description |
|----------|-------------|
| **Inference_ClassicalML.ipynb** | Predict TLE using pretrained Random Forest models. Includes a sample dataset of 34 satellites (9 LEO, 7 GEO, 9 MEO, 9 SSO) retrieved from SpaceTrack.org. Outputs predicted and ground-truth TLE in standard two-line format. |
| **Inference_pretrainedLSTM.ipynb** | Prototype deep learning approach using a pretrained LSTM model trained on a single satellite's historical TLE data. |
| **Apply_SkyField.ipynb** | Converts predicted TLE data into geographic coordinates (Latitude, Longitude, Elevation) and Cartesian positions (X, Y, Z) using the [Skyfield](https://rhodesmill.org/skyfield/) library. Also provides error analysis comparing predictions to ground truth. |



## Benchmark Results

The table below compares Mean Absolute Error (MAE) across different models for each TLE orbital parameter. **Bold values** indicate where the model outperforms the Simple Moving Average (SMA) baseline.
|                     Feature                     | SMA (Baseline) | Ridge Regression |     ARIMA    |     LSTM     |
|:-----------------------------------------------:|:-------------:|:----------------:|:------------:|:------------:|
| First Derivative Mean Motion                    |    3.34E-04   |   **2.73E-04**   | **2.35E-04** | **2.45E-04** |
| Inclination (degrees)                           |    7.64E-04   |   **5.88E-04**   |   1.21E-03   |   1.39E-03   |
| Right Ascension of the Ascending Node (degrees) |    3.98E+01   |   **6.18E+00**   | **3.84E+00** |   1.34E+02   |
| Argument of Perigee (degrees)                   |    3.97E+01   |   **1.81E+01**   |   1.26E+02   |   1.20E+02   |
| Mean Anomaly (degrees)                          |    4.29E+01   |   **3.75E+01**   |   5.40E+01   |   5.67E+01   |
| Eccentricity                                    |    5.80E-05   |   **2.80E-05**   |   1.46E-04   |   1.40E-04   |
| Mean Motion (revolutions per day)               |    2.78E-03   |   **9.43E-04**   |   3.22E-01   |   4.82E-03   |
| Revolution Number at Epoch                      |    1.46E+00   |     1.26E+01     | **1.18E+00** |   4.84E+01   |
<!--
> **Note**
> If you're using Linux Bash for Windows, [see this guide](https://www.howtogeek.com/261575/how-to-run-graphical-linux-desktop-applications-from-windows-10s-bash-shell/) or use `node` from the command prompt.


## Download

You can [download](https://github.com/amitmerchant1990/electron-markdownify/releases/tag/v1.2.0) the latest installable version of Markdownify for Windows, macOS and Linux.

## Emailware

Markdownify is an [emailware](https://en.wiktionary.org/wiki/emailware). Meaning, if you liked using this app or it has helped you in any way, I'd like you send me an email at <bullredeyes@gmail.com> about anything you'd want to say about this software. I'd really appreciate it!

## Credits

This software uses the following open source packages:

- [Electron](http://electron.atom.io/)
- [Node.js](https://nodejs.org/)
- [Marked - a markdown parser](https://github.com/chjj/marked)
- [showdown](http://showdownjs.github.io/showdown/)
- [CodeMirror](http://codemirror.net/)
- Emojis are taken from [here](https://github.com/arvida/emoji-cheat-sheet.com)
- [highlight.js](https://highlightjs.org/)

## Related

[Try Web version of Markdownify](https://notepad.js.org/markdown-editor/)

## Support

If you like this project and think it has helped in any way, consider buying me a coffee!

<a href="https://buymeacoffee.com/amitmerchant" target="_blank"><img src="app/img/bmc-button.png" alt="Buy Me A Coffee" style="height: 41px !important;width: 174px !important;box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;-webkit-box-shadow: 0px 3px 2px 0px rgba(190, 190, 190, 0.5) !important;" ></a>

## You may also like...

- [Pomolectron](https://github.com/amitmerchant1990/pomolectron) - A pomodoro app
- [Correo](https://github.com/amitmerchant1990/correo) - A menubar/taskbar Gmail App for Windows and macOS

## License

MIT

---

> [amitmerchant.com](https://www.amitmerchant.com) &nbsp;&middot;&nbsp;
> GitHub [@amitmerchant1990](https://github.com/amitmerchant1990) &nbsp;&middot;&nbsp;
> Twitter [@amit_merchant](https://twitter.com/amit_merchant)
-->
## Support

This project is supported by National Astronomical Research Institute of Thailand (NARIT).
