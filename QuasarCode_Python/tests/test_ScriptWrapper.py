from QuasarCode.Tools import ScriptWrapper

class Test_ArrayVisuliser(object):
    def test_standard(self):

        def target_function(test_value: int, test_value_2: float, test_value_3: float, test_value_4: float, test_flag: bool, test_flag_2: bool):
            assert test_value == 12345
            assert test_value_2 == 0.12345
            assert test_value_3 == 1.2345
            assert test_value_4 == 12.345
            assert test_flag
            assert not test_flag_2

        wrapper = ScriptWrapper(
            version = "1.0.0",
            authors = [ScriptWrapper.AuthorInfomation(given_name = "Joe", family_name = "Bloggs")],
            description = "A test function.",
            parameters = [
                ScriptWrapper.PositionalParam[int]("test-value", None, None, int, description = "A test parameter."),
                ScriptWrapper.PositionalParam[float]("test-value-2", None, None, float, description = "A test parameter."),
                ScriptWrapper.RequiredParam[float]("test-value-3", "t3", None, float, description = "A test parameter."),
                ScriptWrapper.OptionalParam[float]("test-value-4", "4", None, float, description = "A test parameter."),
                ScriptWrapper.Flag("test-flag", "f", None, description = "A test parameter."),
                ScriptWrapper.Flag("test-flag-2", "f2", None, inverted = True, description = "A test parameter.")
            ]
        )

        wrapper.parse_arguments(["12345", "-t3", "1.2345", "-f", "-4", "12.345", "--test-value-2", "0.12345", "-f2"])

        wrapper.run(target_function)
        