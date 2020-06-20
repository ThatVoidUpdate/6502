# Code Snippets
This is a set of code used for my own reference to make writing the instructions easier
## Addressing Modes:
### Immidiate
```python
    data = machineState["MEMORY"][machineState["PC"] + 1]
```

### ZP
```python
    address = machineState["MEMORY"][machineState["PC"] + 1]
    data = machineState["MEMORY"][address]
```

### ZP,X
```python
    address = machineState["MEMORY"][machineState["PC"] + 1] + machineState["X"]
    data = machineState["MEMORY"][address]
```

### Absolute
```python
    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3])
    data = machineState["MEMORY"][address]
```

### Absolute,X
```python
    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3]) + machineState["X"]
    data = machineState["MEMORY"][address]
```

### Absolute,Y
```python
    address = FromHex(machineState["MEMORY"][machineState["PC"]+1:machineState["PC"]+3]) + machineState["Y"]
    data = machineState["MEMORY"][address]
```

### Indirect,X
```python
    address = machineState["MEMORY"][machineState["PC"] + 1] + machineState["X"]
    finalAddressLowByte = machineState["MEMORY"][address]
    finalAddressHighByte = machineState["MEMORY"][address+1]
    newAddress = FromHex(bytes([finalAddressHighByte, finalAddressLowByte]))
    data = machineState["MEMORY"][newAddress]
```


### Indirect,Y
```python
    address = machineState["MEMORY"][machineState["PC"] + 1]
    finalAddressLowByte = machineState["MEMORY"][address]
    finalAddressHighByte = machineState["MEMORY"][address+1]
    newAddress = FromHex(bytes([finalAddressHighByte, finalAddressLowByte])) + machineState["Y"]
    data = machineState["MEMORY"][newAddress]
```

## Flags:
### Carry
```python
    if machineState["MEMORY"][address] > 0xff: #carry flag
        machineState["MEMORY"][address] -= 0x100
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000001
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111110
```

### Zero
```python
    if machineState["ACC"] == 0x0: #zero flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b00000010
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b11111101
```


### Interrupt Disable
```python
```

### Decimal Mode
```python
```

### Break Command
```python
```

### Overflow
```python
```

### Negative
```python
    if machineState["ACC"] & 0b10000000 == 0b10000000: #negative flag
        machineState["FLAGS"] = machineState["FLAGS"] | 0b10000000
    else:
        machineState["FLAGS"] = machineState["FLAGS"] & 0b01111111
```