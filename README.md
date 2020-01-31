# АПИ Списка продуктов

## Стек технологий

- Python 3.7
- aiohttp
- motor
- mongodb
- Docker + Docker Compose

## Запуск

```text
docker-compose build
docker-compose up -d
```

## API

### Получение продуктов

Запрос:
```text
http GET "127.0.0.1:8080/?limit=10&offset=0&producer=Weimann-Grady"
```

Пример ответа:
```text
HTTP/1.1 200 OK
Content-Length: 232
Content-Type: application/json; charset=utf-8
Date: Fri, 31 Jan 2020 23:09:29 GMT
Server: Python/3.7 aiohttp/3.6.2

[
    {
        "barcode": "60499",
        "photo_url": "http://dummyimage.com/119x191.bmp/5fa2dd/ffffff",
        "price_cents": "27505",
        "producer": "Weimann-Grady",
        "product_name": "Chicken - Breast, 5 - 7 Oz",
        "sku": "d7c3fed8-600c-4ec0-8261-909199741831"
    }
]
```
