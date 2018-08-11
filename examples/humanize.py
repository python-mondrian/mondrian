import mondrian


def main():
    this_is_a_very_long_call_that_is_meant_to_break_everything_but_it_really_needs_to_be_damn_fucking_long_name()


def this_is_a_very_long_call_that_is_meant_to_break_everything_but_it_really_needs_to_be_damn_fucking_long_name():
    raise RuntimeError("This is an error.", "Run `DEBUG=1 <command>` to see the complete stack trace.")


if __name__ == "__main__":
    mondrian.setup(excepthook=True)

    with mondrian.humanizer.humanize():
        main()

    print(mondrian.humanizer.Success('Hello, world.'))
