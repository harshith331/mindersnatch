[![Contributors][contributors-shield]][contributors-url]
[![Forks][forks-shield]][forks-url]
[![Stargazers][stars-shield]][stars-url]
[![Issues][issues-shield]][issues-url]
![Mindersnatch](https://github.com/harshith331/mindersnatch/workflows/Mindersnatch/badge.svg)

<br />
<p align="center">
  <a href="https://github.com/harshith331/mindersnatch">
    <img src="https://raw.githubusercontent.com/othneildrew/Best-README-Template/master/images/logo.png" alt="Logo" width="80" height="80">
  </a>

  <h3 align="center">MINDERSNATCH</h3>

  <p align="center">
    Contributors:
    <br />
    <a href="https://github.com/harshith331"><strong>@harshith331</strong></a>
    <br />
  <a href="https://github.com/romitkarmakar"><strong>@romitkarmakar</strong></a>
    <br />
  <a href="https://github.com/himanshu272"><strong>@himanshu272</strong></a>
    <br />
  <a href="https://github.com/rohitsh16"><strong>@rohitsh16</strong></a>
  </p>
</p>

## Getting Started

To get a local copy up and running follow these simple steps.

### Installation
 
1. Clone the repo
```sh
git clone https://github.com/harshith331/mindersnatch.git
```
2. Create a virtual environment and activate it
```sh
Find it yourself :)
```
3. Change the directory
```sh
cd mindersnatch
```
4. Install the requirements
```sh
pip install -r requirements.txt 
```
5. Copy the .env.example file to .env
```sh
cp .env.example .env
```
6. Make migrations and migrate
```sh
python manage.py makemigrations --settings=msntch.dev_settings && python manage.py migrate --run-syncdb --settings=msntch.dev_settings
```
7. Run server
```sh
python manage.py runserver --settings=msntch.dev_settings
```

## Contributing

Contributions are what make the open source community such an amazing place to be learn, inspire, and create. Any contributions you make are **greatly appreciated**.

1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

<!-- https://www.markdownguide.org/basic-syntax/#reference-style-links -->
[contributors-shield]: https://img.shields.io/github/contributors/harshith331/mindersnatch.svg?style=flat-square
[contributors-url]: https://github.com/harshith331/mindersnatch/graphs/contributors
[forks-shield]: https://img.shields.io/github/forks/harshith331/mindersnatch.svg?style=flat-square
[forks-url]: https://github.com/harshith331/mindersnatch/network/members
[stars-shield]: https://img.shields.io/github/stars/harshith331/mindersnatch.svg?style=flat-square
[stars-url]: https://github.com/harshith331/mindersnatch/stargazers
[issues-shield]: https://img.shields.io/github/issues/harshith331/mindersnatch.svg?style=flat-square
[issues-url]: https://github.com/harshith331/mindersnatch/issues
