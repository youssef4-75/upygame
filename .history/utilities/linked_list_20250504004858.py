class __Node:
    """Node class to represent individual elements in the LinkedList."""
    def __init__(self, data):
        self.data = data  # Data stored in the node
        self.next = None   # Reference to the next node (initially None)
        self.previous = None   # Reference to the previous node (initially None)

class LinkedList:
    """LinkedList class to manage the nodes and operations."""
    def __init__(self):
        self.head = __Node(None)  # Head of the list (initially empty)

    # --- Basic Operations ---
    def is_empty(self):
        """Check if the list is empty."""
        return self.head is None

    def append(self, data):
        """Add a node at the end of the list."""
        new_node = __Node(data)
        if self.is_empty():
            self.head = new_node
        else:
            current = self.head
            while current.next:  # Traverse to the last node
                current = current.next
            current.next = new_node

    def prepend(self, data):
        """Add a node at the beginning of the list."""
        new_node = __Node(data)
        new_node.next = self.head
        self.head = new_node

    def delete(self, data):
        """Delete the first occurrence of a node with given data."""
        if self.is_empty():
            return "List is empty"

        if self.head.data == data:  # Case: Delete head
            self.head = self.head.next
            return

        current = self.head
        while current.next:
            if current.next.data == data:
                current.next = current.next.next  # Skip the node to delete
                return
            current = current.next
        raise ValueError(f"Data '{data}' not found in the list")

    def search(self, data):
        """Check if a node with given data exists."""
        current = self.head
        while current:
            if current.data == data:
                return True
            current = current.next
        return False

    # --- Utility Methods ---
    def size(self):
        """Return the number of nodes in the list."""
        count = 0
        current = self.head
        while current:
            count += 1
            current = current.next
        return count

    def print_list(self):
        """Print all nodes in the list."""
        if self.is_empty():
            print("LinkedList is empty")
            return

        current = self.head
        while current:
            print(current.data, end=" -> " if current.next else "")
            current = current.next
        print()  # Newline

# --- Example Usage ---
if __name__ == "__main__":
    ll = LinkedList()
    ll.append(10)      # 10
    ll.append(20)      # 10 -> 20
    ll.prepend(5)      # 5 -> 10 -> 20
    ll.append(30)      # 5 -> 10 -> 20 -> 30
    ll.delete(10)      # 5 -> 20 -> 30
    ll.print_list()    # Output: 5 -> 20 -> 30
    print("Size:", ll.size())           # Output: 3
    print("Search 20:", ll.search(20))  # Output: True