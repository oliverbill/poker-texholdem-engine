

class EmptyCardDeckException(Exception):
    """Exception raised when a card is requested to be dealt by the CardDeck but it is empty.
        """
    def __init__(self, message="No more cards in the CardDeck"):
        self.message = message
        super().__init__(self.message)
