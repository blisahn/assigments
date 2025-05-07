package structures;

import java.util.ArrayList;
import java.util.List;

public class MinHeap {
    private ArrayList<Integer> heap;

    public MinHeap() {
        this.heap = new ArrayList<>();
    }

    public void insert(int value) {
        heap.add(value);
        heapifyUp(heap.size() - 1);
    }

    public int extractMin() {
        if (isEmpty()) {
            System.out.println("Heap is empty");
            return -1;
        }
        int min = heap.get(0);
        int last = heap.remove(heap.size() - 1);
        if (!isEmpty()) {
            heap.set(0, last);
            heapifyDown(0);
        }
        return min;
    }

    private void heapifyDown(int index) {
        int size = heap.size();
        while (index < size) {
            int left = 2 * index + 1;
            int right = 2 * index + 2;
            int smallest = index;

            if (left < size && heap.get(left) < heap.get(smallest)) {
                smallest = left;
            }
            if (right < size && heap.get(right) < heap.get(smallest)) {
                smallest = right;
            }
            if (smallest == index) {
                break;
            }
            swap(index, smallest);
            index = smallest;
        }
    }

    private void heapifyUp(int index) {
        while (index > 0) {
            int parent = (index - 1) / 2;
            if (heap.get(index) >= heap.get(parent)) {
                break;
            }
            swap(index, parent);
            index = parent;
        }
    }

    private void swap(int i, int j) {
        int temp = heap.get(i);
        heap.set(i, heap.get(j));
        heap.set(j, temp);
    }

    public boolean isEmpty() {
        return heap.size() == 0;
    }

    public int size() {
        int counter = 0;
        for (int i = 0; i < heap.size(); i++) {
            if (heap.get(i) != null) {
                counter++;
            }
        }
        return counter;
    }

    public int findMin() {
        if (isEmpty()) {
            System.out.println("Heap is empty");
            return -1;
        }
        return heap.get(0);
    }
}

class App {
    public static void main(String[] args) throws Exception {

        MinHeap minHeap = new MinHeap();
        minHeap.insert(10);
        minHeap.insert(5);
        minHeap.insert(20);
        minHeap.insert(2);

        System.out.println("Min element: " + minHeap.findMin());
        System.out.println("Extracted Min: " + minHeap.extractMin());
        System.out.println("Min element after extraction: " + minHeap.findMin());
        System.out.println("Heap size: " + minHeap.size());
        System.out.println("Is heap empty? " + minHeap.isEmpty());

        System.out.println("\nTesting heapSort:");
        int[] arr = { 10, 5, 20, 2, 15 };
        List<Integer> sortedList = HeapSort.heapSort(arr);
        System.out.println("Sorted array: " + sortedList);

        System.out.println("\nTesting heapSortDescending:");
        List<Integer> sortedDescending = HeapSortDescending.heapSortDescending(arr);
        System.out.println("Sorted array in descending order: " + sortedDescending);

        System.out.println("\nTesting findKSmallest:");
        int k = 3;
        List<Integer> kSmallest = KSmallest.findKSmallest(arr, k);
        System.out.println("The " + k + " smallest elements: " + kSmallest);

        System.out.println("\nTesting MaxHeap:");
        MaxHeap maxHeap = new MaxHeap();
        maxHeap.insert(10);
        maxHeap.insert(5);
        maxHeap.insert(20);
        maxHeap.insert(2);

        System.out.println("Max element: " + maxHeap.findMax());
        System.out.println("Extracted Max: " + maxHeap.extractMax());
        System.out.println("Max element after extraction: " + maxHeap.findMax());
        System.out.println("Heap size: " + maxHeap.size());
        System.out.println("Is heap empty? " + maxHeap.isEmpty());
    }
}
