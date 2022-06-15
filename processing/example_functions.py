def isThisAKnownTree(type_of_tree_str=None):
    """This function checks the input to see whether it is a recognised tree type,
    it prints to console whether or not it is recognised and returns a suitabel Boolean

    :param type_of_tree_str a string containing the tree type to be tested, defaults to  None
    :type String

    :return: whther or not the input parameters is in th elist of know trees
    :rtype: Boolean
    """
    KNOWN_TREES = ['ash', 'elm', 'oak', 'rowan', 'beech']
    
    if type_of_tree_str.lower() in KNOWN_TREES:

        print(f'I recognise this tree: {type_of_tree_str}')
        return True
    else:

        print(f'I do not recognise this tree: {type_of_tree_str}')
        return False
