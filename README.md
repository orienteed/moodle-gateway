<img src="./resources/B2BStoreLogo.svg" width="" height="90" align = "left">
<h1>Moodle Gateway</h1>

</br>

#### Table of Contents

- [📢 What is Moodle Gateway?](#-what-is-moodle-gateway)
- [🛒 Supported Platforms](#-supported-platforms)
- [✅ Requirements](#-requirements)
- [⚙️ Installation](#%EF%B8%8F-installation)
- [🙌🏼 How to contribute](#-how-to-contribute)

</br>

## 📢 What is Moodle Gateway?

Moodle Gateway is an excellent tool for those who want to integrate Moodle with external systems but don't have the knowledge or time to develop a custom integration.

It is an intermediate API that encapsulates/handles the authentication and requests to the Moodle API (like a wrapper) and exposes some endpoints to interact with them. The Gateway is a straightforward and effective way to integrate Moodle with third-party systems.

This software can be installed on a server and configured to listen for incoming requests from external systems. It then forwards those requests to Moodle using the Moodle Helpdesk API.

</br>

## 🛒 Supported Platforms

<table>
  <tr>
    <td align="center"><a href="https://business.adobe.com/products/magento/magento-commerce.html"><img src="./resources/MagentoLogo.svg" width="60" height="60" alt=""/><br /><sub><b>Magento</b></sub></a><br /></td>
    <td align="center"><a href="https://www.orienteed.com/en/blog"><img src="./resources/ComingSoon.png" width="60" height="60" alt=""/><br /><sub><b>Stay tuned!</b></sub></a><br /></td>
  </tr>
</table>

</br>

## ✅ Requirements

The requirements are:

- <a href="https://moodle.org/" target="_blank">Moodle</a>

To use Moodle Gateway you need to have a Moodle instance up and running. You can install it using the <a href="https://docs.moodle.org/400/en/Installation" target="_blank">Moodle installation guide</a>.

- <a href="https://docs.docker.com/get-started/overview/" target="_blank">Docker</a>
- <a href="https://docs.docker.com/compose/" target="_blank">Docker Compose</a>

Docker and docker-compose are also required. If you don't have them installed, you can follow the <a href="https://docs.docker.com/engine/install/" target="_blank">Docker installation guide</a> and the <a href="https://docs.docker.com/compose/install/" target="_blank">Docker Compose installation guide</a>.

</br>

## ⚙️ Installation

To install Moodle Gateway you need to follow these steps:

1. Clone the repository with:

```
git clone https://github.com/orienteed/moodle-gateway
```

2. Copy the _.env.example_ file to _.env_.
3. Fill _.env_ file with the required data.
4. Run the following command to start the gateway:

```
docker-compose up -d --build
```

5. Now your gateway is running, you can see an endpoints summary in <a href="http://localhost:8082/docs" target="_blank">http://localhost:8082/docs</a>

</br>

<div align="center">
<b>
🚀 You can test every request using our Postman collection, click <a href="./resources/GatewayPostmanCollection.json" target="_blank">here</a> to download it 🚀
</b>
</div>

</br>

## 🙌🏼 How to contribute

To contribute to this project, you can do it in the following ways:

- Reporting bugs.
- Suggesting enhancements.
- Opening pull requests.

If you want to know more, please <a href="https://www.b2bstore.io/contact" target="_blank">contact us</a>

<hr>

<div align="center">
    <h3>Developed by</h3>
    <a href="https://www.orienteed.com/" target="_blank"><img src="./resources/OrienteedLogo.svg" width="" height="90" align = "middle"></a>
</div>
