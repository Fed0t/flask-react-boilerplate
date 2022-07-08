from flasgger import Swagger
template = {
  "swagger": "2.0",
  "info": {
    "title": "Api Documentation",
    "description": "API Data",
    "contact": {
      "responsibleOrganization": "ME",
      "responsibleDeveloper": "Me",
      "email": "serghei@veelancing.io",
      "url": "invoicecash.com",
    },
    "termsOfService": "http://me.com/terms",
    "version": "0.0.1"
  },
  "basePath": "/api/v1/",
  "schemes": [
    "http",
    "https"
  ],
  "operationId": "getmyData"
}

swagger_config = {
    "headers": [
    ],
    "specs": [
        {
            "endpoint": 'apispec_1',
            "route": '/api/v1/docs/apispec_1.json',
            "rule_filter": lambda rule: True,  # all in
            "model_filter": lambda tag: True,  # all in
        }
    ],
    "static_url_path": "/api/v1/docs/static",
    "swagger_ui": True,
    "specs_route": "/api/v1/docs/"
}


swagger = Swagger(template=template, config=swagger_config)