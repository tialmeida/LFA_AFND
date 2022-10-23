import asyncio


def inputLineBreak(text):
    if PRINT_QUESTIONS:
        return input(f'{text}\n')
    else:
        return input()


def printNot():
    print("N")


def printYes():
    print("S")


def ifNotContainsRaiseException(array, object_to_validate):
    if not any(array_object for array_object in array if array_object == object_to_validate):
        raise Exception()


def validateSymbol(symbol_to_validate):
    ifNotContainsRaiseException(alphabet, symbol_to_validate)


def validateState(state_to_validation):
    ifNotContainsRaiseException(states, state_to_validation)


async def go_through(first_state, word_remaining, final_states):
    current_state = first_state

    for index, symbol in enumerate(word_remaining):
        if await processEmptyWord(symbol, current_state, word_remaining[index + 1:], final_states):
            current_state = ERROR_STATE
            break

        try:
            next_states = states[current_state][symbol]
            if len(next_states) > 1:
                for next_state in next_states:
                    await go_through(next_state, word_remaining[index + 1:], final_states)
                    current_state = ERROR_STATE
                break
            else:
                current_state = next_states[0]
        except:
            current_state = ERROR_STATE
            break

    if current_state is not ERROR_STATE:
        final_states.append(current_state)


async def processEmptyWord(symbol, current_state, word_remaining, final_states):
    try:
        if symbol is EMPTY_WORD:
            raise Exception()

        next_states = states[current_state][EMPTY_WORD]

        for next_state in next_states:
            await go_through(next_state, word_remaining, final_states)

        return True
    except:
        return False



ERROR_STATE = 'ERROR'
EMPTY_WORD = '*'
PRINT_QUESTIONS = False

states_aux = inputLineBreak("Digite os estados")
states_aux = states_aux.split()

alphabet = inputLineBreak("Digite o alfabeto")
alphabet = alphabet.split()

transtionsNumber = int(inputLineBreak("Digite o número total de transições"))

states = {}

for state_aux in states_aux:
    states[state_aux] = {}

for index in range(0, transtionsNumber):
    transtion = inputLineBreak("Digite a transição").split()
    validateState(transtion[0])
    validateState(transtion[2])
    validateSymbol(transtion[1])

    try:
        states[transtion[0]][transtion[1]].append(transtion[2])
    except KeyError:
        states[transtion[0]][transtion[1]] = [transtion[2]]

start_state = inputLineBreak("Digite o estado incial")
if len(states) > 0:
    validateState(start_state)

end_states = inputLineBreak("Digite os estados finais").split()
for end_state in end_states:
    validateState(end_state)

words = inputLineBreak("Digite as palavras").split()

# final_states = []


async def main():
    for word in words:
        final_states = []
        await go_through(start_state, word, final_states)

        accept = False
        for final_state in final_states:
            if any(state for state in end_states if state == final_state):
                accept = True
                break

        if accept:
            printYes()
        else:
            printNot()

asyncio.run(main())
