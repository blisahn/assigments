package structures;

import java.util.ArrayList;
import java.util.List;

public class KSmallest {
    public static List<Integer> findKSmallest(int[] arr, int k) {
        MinHeap minHeap = new MinHeap();

        for (int num : arr) {
            minHeap.insert(num);
        }
        List<Integer> smallestK = new ArrayList<>();
        for (int i = 0; i < k; i++) {
            if (!minHeap.isEmpty()) {
                smallestK.add(minHeap.extractMin());
            }
        }
        return smallestK;
    }
}
