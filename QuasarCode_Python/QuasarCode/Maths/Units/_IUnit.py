class IUnit(object):
    """
    Provides a link between ordenary and compound unit types
    """
    def GetFundamentalUnitPairs(self):
        """
        Allows compatibility between ordenary and compound unit types by providing common access to their data

        Returns:
            An array of FundamentalUnitPowerPair representing all units in the object
        """
        raise NotImplementedError("This method MUST be overriden in a child class.")

    def GetUnitPairs(self):
        """
        Allows compatibility between ordenary and compound unit types by providing common access to their data

        Returns:
            An array of UnitPowerPairs representing all units in the object
        """
        raise NotImplementedError("This method MUST be overriden in a child class.")

    def ToString(self):
        """
        Provides a string representation of the unit

        Returns:
            The unit as a string
        """
        raise NotImplementedError("This method MUST be overriden in a child class.")

    def __str__(self):
        try:
            return self.ToString()
        except NotImplementedError:
            raise NotImplementedError("The method \"ToString\" MUST be overriden in a child class.")

    def Pow(self, p):
        """
        Raises a unit to a power

        Paramiters:
            int p -> The power

        Returns:
            IUnit
        """
        raise NotImplementedError("This method MUST be overriden in a child class.")

    def Mult(self, u):
        """
        Multiplies a unit by annother

        Paramiters:
            IUnit u -> The unit to multyply by

        Returns:
            IUnit
        """
        raise NotImplementedError("This method MUST be overriden in a child class.")

    def Div(self, u):
        """
        Divides a unit by annother

        Paramiters:
            IUnit u -> The unit to divide this by

        Returns:
            IUnit
        """
        raise NotImplementedError("This method MUST be overriden in a child class.")