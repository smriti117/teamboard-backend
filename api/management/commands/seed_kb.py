from django.core.management.base import BaseCommand

from api.models import KBEntry

ENTRIES = [
    {
        "question": "What is select_related in Django ORM?",
        "answer": "select_related performs a SQL JOIN and fetches related objects "
                  "in the same query, avoiding extra round trips for ForeignKey "
                  "and OneToOneField relationships.",
        "category": KBEntry.Category.DATABASE,
    },
    {
        "question": "How does prefetch_related differ from select_related?",
        "answer": "prefetch_related runs a separate query per relation and joins "
                  "the results in Python, which works for ManyToMany and reverse "
                  "ForeignKey relations that select_related cannot handle.",
        "category": KBEntry.Category.DATABASE,
    },
    {
        "question": "How does transaction.atomic() work?",
        "answer": "transaction.atomic() wraps a block of database operations so "
                  "they either all commit or all roll back together, preventing "
                  "partial writes if an error occurs mid-block.",
        "category": KBEntry.Category.DATABASE,
    },
    {
        "question": "What is a JWT token?",
        "answer": "A JWT (JSON Web Token) is a signed, self-contained token used "
                  "for stateless authentication. The server issues it after login "
                  "and the client sends it with each request to prove identity.",
        "category": KBEntry.Category.API,
    },
    {
        "question": "How does JWT authentication differ from session authentication?",
        "answer": "JWT authentication is stateless — the token itself carries the "
                  "identity claim and the server verifies its signature — whereas "
                  "session authentication relies on server-side session storage.",
        "category": KBEntry.Category.API,
    },
    {
        "question": "When should I use Q objects?",
        "answer": "Q objects let you build complex queries with OR conditions or "
                  "nested AND/OR logic that plain keyword filtering in .filter() "
                  "cannot express, e.g. Q(a=1) | Q(b=2).",
        "category": KBEntry.Category.DATABASE,
    },
    {
        "question": "How do Django signals work?",
        "answer": "Signals let decoupled pieces of code get notified when actions "
                  "occur elsewhere. post_save fires after a model instance is "
                  "saved, commonly used to auto-create related objects.",
        "category": KBEntry.Category.FRAMEWORK,
    },
    {
        "question": "What is a REST API?",
        "answer": "A REST API exposes resources over HTTP using standard verbs "
                  "(GET, POST, PUT, DELETE) and status codes, typically "
                  "exchanging data as JSON.",
        "category": KBEntry.Category.API,
    },
    {
        "question": "What is horizontal scaling in cloud infrastructure?",
        "answer": "Horizontal scaling adds more machines to handle load, as "
                  "opposed to vertical scaling which adds more resources to a "
                  "single machine. Cloud platforms make this elastic and on-demand.",
        "category": KBEntry.Category.CLOUD,
    },
    {
        "question": "What is a load balancer?",
        "answer": "A load balancer distributes incoming traffic across multiple "
                  "servers to improve availability and prevent any single server "
                  "from being overwhelmed, often used alongside horizontal scaling.",
        "category": KBEntry.Category.CLOUD,
    },
    {
        "question": "What is Docker used for?",
        "answer": "Docker packages an application with its dependencies into a "
                  "container that runs consistently across environments, commonly "
                  "used to run services like PostgreSQL locally.",
        "category": KBEntry.Category.CLOUD,
    },
    {
        "question": "What is middleware in Django?",
        "answer": "Middleware is a chain of hooks that process requests and "
                  "responses globally, e.g. for authentication, CORS, or logging, "
                  "before a request reaches a view or after a view returns.",
        "category": KBEntry.Category.FRAMEWORK,
    },
]


class Command(BaseCommand):
    help = "Seed the knowledge base with sample Q&A entries."

    def handle(self, *args, **options):
        created = 0
        for entry in ENTRIES:
            _, was_created = KBEntry.objects.get_or_create(
                question=entry["question"],
                defaults={"answer": entry["answer"], "category": entry["category"]},
            )
            if was_created:
                created += 1
        self.stdout.write(
            self.style.SUCCESS(f"Seeded {created} new KB entries (total: {KBEntry.objects.count()}).")
        )
