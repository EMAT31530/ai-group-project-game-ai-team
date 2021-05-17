
<!-- PROJECT LOGO -->
<br />
<p align="center">
  <a href="https://github.com/EMAT31530/ai-group-project-game-ai-team">
    <img src="images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">Poker Ai via CFRs</h3>

  <p align="center">
    Employing various methods of Counterfactual Regret Minimization to generate Kuhn, Leduc, and HULH poker AIs. 
    Those methods being: vanilla cfr (scalar/simultanious, vector/alternating), cfr+, the various sampling forms of mccfr (PCS, OPCS, SPCS, CS), and finally outcome sampling cfr.
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
If you want to train an ai, first cd to the Tests folder in your terminal, then run 
```terminal
python leductest.py 6 1000 0 1
```
or 
```terminal
python kuhntest.py 1 10000 0 1
```
The first index specifies the method used, 1: Vanilla CFR (scalar/simultanious), 2: Outcome Sampling Cfr, 3: Chance Sampling, 4: Vanilla (vector/alternating), 5: Public CS, 6: OpponentPublic CS, 7: SelfPublic CS, 8: CFR+.
The second index is the number of iterations performed.
The third index is if you wish exploitability and various other metrics to be calculated.
The fourth index is if you wish to export the trained strategy map to a .Json file, found in Trainer/Strategy.

For more specifics see the various ____test.py files.

You can also play against the AIs within TerminalPlayer by first moving over a strategy to the strategy folder within TerminalPlayer then running 
```terminal
python game.py k AIKuhn
```
The first index specifies the type of game to play, 'k': Kuhn, 'l': Leduc. The second index is the name of the AI strategy file to use.
For more specifics see the file.

<!-- ROADMAP -->
## Roadmap
Write a better readme.

<!-- ACKNOWLEDGEMENTS -->
## Acknowledgements

* [Terminal playing cards](https://github.com/pwildenhain/terminal_playing_cards)
* [README-Template](https://github.com/othneildrew/Best-README-Template/blob/master/BLANK_README.md)