

### Handle invalid requests
```python
# old way
if not serializer.is_valid():
    raise ValidationError(serializer.errors)
    # or
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# cleaner way
serializer.is_valid(raise_exception=True)
```

Cách đơn giản nhất để set id cho một object đấy là tạo fixture rồi chạy loaddata.



