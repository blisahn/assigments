package structures;

import java.util.ArrayList;
import java.util.List;

public class HeapSortDescending {
    public static List<Integer> heapSortDescending(int[] arr) {
        MaxHeap maxHeap = new MaxHeap();
        for (int num : arr) {
            maxHeap.insert(num);
        }

        List<Integer> sortedList = new ArrayList<>();
        while (!maxHeap.isEmpty()) {
            sortedList.add(maxHeap.extractMax());
        }
        return sortedList;
    }
}
