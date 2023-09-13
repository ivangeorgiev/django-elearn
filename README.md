# django-elearning
Sample Project: E-Learning Platform in Django

```mermaid
erDiagram
    Subject ||..o{ Course : has
    Course ||..o{ Module : has
    Module ||..o{ Content : has
    Content ||..o{ ItemBase : contains

    ItemBase ||--o| Text : is
    ItemBase ||--o| File : is
    ItemBase ||--o| Image : is
    ItemBase ||--o| Video : is
```
