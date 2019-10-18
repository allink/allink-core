#### Dummy App   
This is a dummy app which will be used to create new apps via management command "new_app" in client projects. The complete directory (except this README.md) will be copied and modified to match the naming of the new app.

> This dummy app will be used as an template whenever we want to filter entries with an AllinkBaseAppContentPlugin

The model which will be created has the following characteristics by default:
- can be tagged with AllinkCategory
- has all the fields from AllinkMetaTagMixin and AllinkTeaserMixin
- is sortable in admin
- has a detail view
