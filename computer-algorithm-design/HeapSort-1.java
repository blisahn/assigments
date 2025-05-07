package structures;

import java.util.ArrayList;
import java.util.List;

public class HeapSort {

    public static List<Integer> heapSort(int[] arr) {
        MinHeap minHeap = new MinHeap();
        for (int num : arr) {
            minHeap.insert(num);
        }

        List<Integer> sortedList = new ArrayList<>();
        while (!minHeap.isEmpty()) {
            sortedList.add(minHeap.extractMin());
        }
        return sortedList;
    }
}
