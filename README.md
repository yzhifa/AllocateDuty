# A Resource Allocation Problem

### Problem
A _m_ man team has to fulfill a 12-hour monitoring obligation daily every week. For a 8 (_m_ = 8) man team, this is easily allocated as such:
- 2 personnel cover the weekdays (5-days).
- remaining 6 personnel cover the weekends; each personnel covers a 4-hour shift.

There are constraints to the allocation:
- Each personnel should not work more than 3 weekdays per month.
- If a personnel is allocated to weekday duties on a week, he will not be allocated a weekend shift on that week.

The aim of the code is to generalize the allocation in anticipation to a growing team size so that the allocation is as fair as possible.

(A personal challenge is to use as few packages as possible. I have coded this using only NumPy.)

### Approach

Generally, a (_m_ by 11) array is created to allocate the weekly schedule. An allocation is denoted 1, and 0 otherwise.

The scheduled array is then multiplied by a cost vector (1 by 11) to calculate the total hours worked for each _m_ member. The total hours worked/allocated to the members are then memoized for optimization later.

The subsequent schedules are created and optimized heuristically - generate 500 schedules for that week and find out which schedule has the least spread in terms of the total hours allocated per member. (It turns out that there is no need to track whether a personnel is allocated weekday duties.)

### Conclusion

Based on the current allocation constraints, the mean and standard deviation of the hours each personnel has to work for a year for a 8-man team is 546 and 8.25 respectively (after 100 simulations).

This means that there is a chance someone may have to do 2 to 4 more weekend duties, or about 1 extra weekday, or a combination of both.

In summary, this is as fair as it gets.





