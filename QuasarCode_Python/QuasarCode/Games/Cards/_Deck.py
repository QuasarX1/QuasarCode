from QuasarCode.edp import Event
from QuasarCode.Games.Cards import CardGroup, PlayingCard
from random import Random

class Deck(CardGroup):
    """
    A collection of 52+ unique playing cards. The exact number can vary dependant on the number of jokers added

    Atributes:
        str Name --> name of the collection
        int Jokers --> the number of jokers in this deck
        list[IPlayingCard] Cards --> the cards in the deck (including the jokers)
        QuasarCode.edp.Event ReturnCards --> request that all subscribers remove their held card objects

    __init__():
        str name --> name of the collection
        int jokers --> the number of jokers in this deck
    """
    def __init__(self, name: str, jokers: int = 0):
        self.Jokers: int = jokers
        self.Cards: list = []

        for suit in PlayingCard.AllowedSuits:
            if suit != PlayingCard.AllowedSuits.J:
                for value in PlayingCard.AllowedValues:
                    if value != PlayingCard.AllowedValues.Jo:
                        self.Cards.append(PlayingCard(value, suit))

        for i in range(jokers):
            self.Cards.append(PlayingCard(PlayingCard.AllowedValues.Jo, PlayingCard.AllowedSuits.J))

        super().__init__(name, self.Cards)

        self.__subscribers = []
        self.ReturnCards = Event()

    def InitialiseGroup(self, groups: list):
        """
        Initialises a card group for use with the deck

        Paramiters:
            list[CardGroup] groups --> the group(s) to be initialised
        """
        for group in groups:
            if group not in self.__subscribers:
                self.__subscribers.append(group)
                self.ReturnCards += group.ReturnCards

    def ReleaseGroup(self, groups: list):
        """
        Removes card groups from use with the deck

        Paramiters:
            list[CardGroup] groups --> the group(s) to remove
        """
        for group in groups:
            if group in self.__subscribers:
                self.__subscribers.remove(group)
                self.ReturnCards -= group.ReturnCards

    def Deal(self, hands: list, cardsPerHand: int = None, remainderGroups: list = None, suppressEmptyException: bool = False):
        """
        Either:
        1.) Deals the deck into a list of groups untill the deck is empty
            if only first paramiter is set

        2.) Deals a set number of cards from the deck into a list of groups and then deals the remaining cards to a list of groups if avalable

        Paramiters:
            list[CardGroup] hands --> The hands to deal into. Set only this paramiter for result (1)
            int cardsPerHand --> The number of cards to deal to each hand (deafult is None)
            list[CardGroup] remainderGroups --> The groups to deal any remaining cards into (deafult is None)
            bool suppressEmptyException --> Whether or not to suppress the exception generated when there isn't enough cards remaining to fill deal the number requested to each hand (deafult is False)
        """
        for hand in hands:
            if hand not in self.__subscribers:
                raise ValueError("One of the card groups provided wasn't initialised for use with this deck.")

        if remainderGroups is not None:
           for group in remainderGroups:
              if group not in self.__subscribers:
                raise ValueError("One of the remainder groups provided wasn't initialised for use with this deck.")

        randomiser = Random()

        if cardsPerHand == None:
            while len(self) > 0:
                for hand in hands:
                    if len(self) > 0:
                        hand.append(self.Remove(randomiser.randint(0, len(self))))
                    else:
                        break

        else:
            if not suppressEmptyException and cardsPerHand * lan(hands) > len(self):
                raise ValueError("There aren't enough cards in the deck to do this.")

            for i in range(cardsPerHand):
                for hand in hands:
                    if len(self) > 0:
                        hand.append(self.Remove(randomiser.randint(0, len(self))))
                    else:
                        break

                if len(self) == 0:
                    break

            if remainderGroups is not None:
                self.Deal(remainderGroups)

    def Reset(self):
        """
        Reset the deck so that it has all the cards it started with and asks all ICardGroups dealt to to remove references to the cards
        """
        self.clear()

        if len(self.__subscribers) > 0:
            self.ReturnCards.run(self)
        
        for card in self.Cards:
            self.append(card)