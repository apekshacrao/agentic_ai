from library_data import library_data


def _normalise(message):
    return " ".join(str(message or "").lower().strip().split())


def _book_details(book):
    return (
        f"📚 {book['title']}\n"
        f"👤 Author: {book['author']}\n"
        f"📖 Subject: {book['subject']}\n"
        f"📍 Rack: {book['rack']}\n"
        f"🏢 Department: {book.get('department', 'Not specified')}\n"
        f"✅ Available copies: {book['available']}"
    )


def chatbot_response(message):
    message = _normalise(message)

    if not message:
        return "Please enter a question about the library."

    words = set(message.replace("?", "").replace("!", "").replace(".", "").split())

    # Goodbye
    if words.intersection({"bye", "goodbye", "thanks", "thank"}):
        return "Goodbye! Happy reading! 👋"

    # Greeting
    if words.intersection({"hello", "hi", "hey", "help"}):
        return (
            "Hello! 👋 I am the CMRIT Library Assistant.\n\n"
            "You can ask me about:\n"
            "📚 Books\n"
            "📍 Book locations\n"
            "🕐 Library timings\n"
            "📜 Rules\n"
            "📖 Borrowing\n"
            "✅ Book availability\n"
            "🔎 Search by title, author, or subject"
        )

    # Library timings
    if (
        "timing" in message
        or "timings" in message
        or "library time" in message
        or "library timing" in message
    ):
        timings = library_data["library"]["timings"]

        return (
            "📚 CMRIT Library Timings:\n\n"
            f"Monday-Friday: {timings['monday_to_friday']}\n"
            f"Saturday: {timings['saturday']}\n"
            f"Sunday: {timings['sunday']}"
        )

    # Library location
    if (
        "where is library" in message
        or "library location" in message
        or "library located" in message
        or message == "location"
    ):
        return (
            f"📍 {library_data['library']['name']}\n"
            f"Location: {library_data['library']['location']}"
        )

    # Borrowing information
    if ("borrow" in message or "issue" in message
            or "how many books" in message or "loan" in message):
        student_info = library_data["borrowing"]["students"]

        return (
            "📖 Student Borrowing Information:\n\n"
            f"Maximum books: {student_info['maximum_books']}\n"
            f"Loan period: {student_info['loan_period']}"
        )

    # Library rules
    if "rule" in message or "rules" in message or "allowed" in message:
        rules = library_data["rules"]

        response = "📜 Library Rules:\n\n"

        for i, rule in enumerate(rules, start=1):
            response += f"{i}. {rule}\n"

        return response.rstrip()

    # Rack Finder
    rack_keywords = [
        "where is",
        "where can i find",
        "rack",
        "location of",
        "located",
        "find"
    ]

    if any(keyword in message for keyword in rack_keywords):

        for book in library_data["books"]:

            title = book["title"].lower()
            subject = book["subject"].lower()
            author = book["author"].lower()

            if (
                title in message
                or subject in message
                or author in message
            ):
                return _book_details(book)

    # Available books
    if "available" in message and (
        "book" in message or "books" in message
    ):
        available_books = [
            book
            for book in library_data["books"]
            if book["available"] > 0
        ]

        if not available_books:
            return "Sorry, no books are currently available."

        response = "📚 Available Books:\n\n"

        for book in available_books:
            response += (
                f"• {book['title']}\n"
                f"  📖 {book['subject']}\n"
                f"  📍 Rack: {book['rack']}\n"
                f"  ✅ {book['available']} copies\n\n"
            )

        return response.rstrip()

    # Book search by title, author, subject, or meaningful subject words.
    for book in library_data["books"]:

        title = book["title"].lower()
        author = book["author"].lower()
        subject = book["subject"].lower()

        subject_words = {word for word in subject.split() if len(word) > 2}
        if (title in message or author in message or subject in message
                or subject_words.intersection(message.split())):

            if book["available"] > 0:
                return _book_details(book)

            return (
                f"📚 {book['title']} is currently unavailable."
            )

    # Show all books
    if "books" in message or "book" in message:

        response = "📚 Available Books:\n\n"

        for book in library_data["books"]:
            response += (
                f"• {book['title']} - "
                f"{book['subject']}\n"
            )

        return response.rstrip()

    # Default response
    return (
        "Sorry, I couldn't understand that. 😅\n\n"
        "Try asking:\n"
        "• What are the library timings?\n"
        "• Where is the DBMS book?\n"
        "• Where can I find Operating Systems?\n"
        "• How many books can I borrow?\n"
        "• What are the library rules?\n"
        "• Show me available books."
    )