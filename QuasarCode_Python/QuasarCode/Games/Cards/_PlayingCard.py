from QuasarCode.Games.Cards import IPlayingCard
from enum import Enum

class PlayingCard(IPlayingCard):
    """
    A card from a standard deck of 52 playing cards

    Atributes:
        PlayingCard.AllowedValues Value --> The card's value
        PlayingCard.AllowedSuits Suit --> The card's suit
    """

    class AllowedValues(Enum):
        """
        Enum of card values from ace to king and joker
        """
        
        A = 0,# Ace

        Two = 1,# Two

        Three = 2,# Three

        Four = 3,# Four

        Five = 4,# Five

        Six = 5,# Six

        Seven = 6,# Seven

        Eight = 7,# Eight

        Nine = 8,# Nine

        Ten = 9,# Ten

        J = 10,# Jack

        Q = 11,# Queen

        K = 12,# King

        Jo = 13# Joker

    class AllowedSuits(Enum):
        """
        Enum of card suits - hearts, clubs, dimonds, spades, joker
        """
        
        H = 0,# Heart

        C = 1,# Club

        D = 2,# Dimond

        S = 3,# Spade

        J = 4# Joker

    def __init__(self, value: AllowedValues, suit: AllowedSuits):
        self.__value = value
        self.__suit = suit

    @property
    def Value(self) -> AllowedValues:
        """
        The card's value
        """
        return self.__value

    @property
    def Suit(self) -> AllowedSuits:
        """
        The card's suit
        """
        return self.__suit

    __ValueStrings = ("A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K")

    def GetValueString(value: AllowedValues) -> str:
        """
        Retrive the string counterpart to the AllowedValues enum value
        """
        return PlayingCard.__ValueStrings[int(value)]

    __SuitStrings = ("Heart", "Club", "Dimond", "Spade", "Joker")

    def GetSuitString(suit: AllowedSuits) -> str:
        """
        Retrive the string counterpart to the AllowedSuits enum suit
        """
        return PlayingCard.__SuitStrings[int(suit)]