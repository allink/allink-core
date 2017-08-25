# Introduction

This doc specifies the way allink-core is ment to be used. It will also give some usefull tips on how to get started. It will not however cover the technical details of its underliing codebase.
allink-core is ment to be used with our boilerplate project which is hosted on the [divio cloud](https://www.divio.com/en/). (feel free to send us a [message](mailto:itcrowd@allink.ch) if you would like to have a look.)

The steps we describe here are mostly closly coupled to our setup and environment. So the described steps might not make sense to you, when you don't know our setup. Also we skip steps which we already included in the boilerplate.

# The idea behind allink-core
allink-core was implemented to create a standardized ecosystem for applications developed at [allink AG](https://www.allink.ch). Amongst other things it contains mostly django apps, django-cms plugins to provide patterns to solve recurring problems and usecases. The underling question when developing on core functionallity should always be "Is it going to be reused again?"