from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from apispec_webframeworks.flask import FlaskPlugin
# from apispec_fromfile import FromFilePlugin
from marshmallow import Schema, fields
from app.models import UserSchema, StripeSchema

spec = APISpec(
    title="My App",
    version="1.0.0",
    openapi_version="3.0.2",
    plugins=[FlaskPlugin(), MarshmallowPlugin()],
)
print(2222222222222222222222, spec.to_yaml())
spec.components.schema("User", schema=UserSchema)
spec.components.schema("Stripe", schema=StripeSchema)

tags = [
            {'name': 'User',
             'description': 'User API for several operations.'
            },
            {'name': 'stripe functions',
             'description': 'For stripe functions'
            },
       ]

for tag in tags:
    print(f"Adding tag: {tag['name']}")
    spec.tag(tag)

