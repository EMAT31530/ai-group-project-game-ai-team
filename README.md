
<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/EMAT31530/ai-group-project-game-ai-team">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Poker Ai via CFR</h3>

  <p align="center">
    Employing various methods of Counterfactual Regret Minimization to generate Kuhn, Leduc, and Texas Hold'dem poker AIs. 
    Those methods being: vanilla cfr (scalar/simultanious, vector/alternating), cfr+, the various sampling forms of mccfr (PCS, SPCS, CS), and finally outcome sampling cfr.
    <br />
  </p>
</p>

<!-- TABLE OF CONTENTS -->
<details open="open">
  <summary><h2 style="display: inline-block">Table of Contents</h2></summary>
  <ol>
    <li>
      <a href="#about-the-project">About The Project</a>
      <ul>
        <li><a href="#built-with">Built With</a></li>
      </ul>
    </li>
    <li>
      <a href="#getting-started">Getting Started</a>
      <ul>
        <li><a href="#prerequisites">Prerequisites</a></li>
        <li><a href="#installation">Installation</a></li>
      </ul>
    </li>
    <li><a href="#usage">Usage</a></li>
    <li><a href="#roadmap">Roadmap</a></li>
    <li><a href="#acknowledgements">Acknowledgements</a></li>
  </ol>
</details>



<!-- ABOUT THE PROJECT -->
## About The Project

it was fun :)

### Built With

* []()
* []()
* []()



<!-- GETTING STARTED -->
## Getting Started

To get a local copy up and running follow these simple steps.

### Prerequisites

This is an example of how to list things you need to use the software and how to install them.
* pip
  ```sh
  pip install terminal-playing-cards
  ```

### Installation

1. Clone the repo
   ```sh
   git clone https://github.com/EMAT31530/ai-group-project-game-ai-team.git
   ```

<!-- USAGE EXAMPLES -->
## Usage
If you want to run a training you do the ole 
```terminal
python leductest.py 6 1000 0 1
```
or 
```terminal
python kuhntest.py 1 10000 0 1
```
The first index specifies the method used, 1: Vanilla CFR (scalar/simultanious), 3: Outcome Sampling Cfr, 4: Chance Sampling, 5: Vanilla (vector/alternating), 6: Public CS, 8: SelfPublic CS, 9: CFR+.
The second index is the number of iterations.
The third index is if you want exploitability to be calculated.
The fourth index is if you want to export the finalised strategy map to a .Json file.

For more specifics see the various test.py files...

You can also play against the AIs by running 
```terminal
python testgame.py
```
check it for choosing which gametype etc. 

<!-- ROADMAP -->
## Roadmap
Write a better readme.

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [Terminal playing cards](https://github.com/pwildenhain/terminal_playing_cards)
* [README-Template](https://github.com/othneildrew/Best-README-Template/blob/master/BLANK_README.md)