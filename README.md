# iOS Tools

## 1. Create template:

### 1.1. Base template:

```
$ python it.py template -base <Scene_Name>
```

For example:
```
$ python it.py template -base Login
 
        new file:   Login/LoginViewModel.swift
        new file:   Login/LoginNavigator.swift
        new file:   Login/LoginUseCase.swift
        new file:   Login/LoginViewController.swift
        new file:   Login/Test/LoginViewModelTests.swift
        new file:   Login/Test/LoginUseCaseMock.swift
        new file:   Login/Test/LoginNavigatorMock.swift
        new file:   Login/Test/LoginViewControllerTests.swift
 
Finish!
```

### 1.2. List template:

Copy model text to clipboard then using command:
```
$ python it.py template -list <Scene_Name> [--section]
```

*Option*:
--section: Display list item with header sections.


For example :

Copy json text to clipboard:
```
struct Product {
    let id: Int
    let name: String
    let price: Double
}
```

then using command:
```
 $ python it.py template -list ProductList

        new file:   ProductList/ProductListViewModel.swift
        new file:   ProductList/ProductListNavigator.swift
        new file:   ProductList/ProductListUseCase.swift
        new file:   ProductList/ProductListViewController.swift
        new file:   ProductList/ProductCell.swift
        new file:   ProductList/Test/ProductListViewModelTests.swift
        new file:   ProductList/Test/ProductListUseCaseMock.swift
        new file:   ProductList/Test/ProductListNavigatorMock.swift
        new file:   ProductList/Test/ProductListViewControllerTests.swift
        new file:   ProductList/Test/ProductCellTests.swift
 
Finish!
```

### 1.3. Detail template:

Copy model text to clipboard then using command:
```
$ python it.py template -detail <Scene_Name> [--static]
```

*Option*:
--static: Display item detail in static UITableView.


For example :

Copy json text to clipboard:
```
struct Product {
    let id: Int
    let name: String
    let price: Double
}
```

then using command:
```
 $ python it.py template -detail ProductDetail
 
        new file:   ProductDetail/ProductDetailViewModel.swift
        new file:   ProductDetail/ProductDetailNavigator.swift
        new file:   ProductDetail/ProductDetailUseCase.swift
        new file:   ProductDetail/ProductDetailViewController.swift
        new file:   ProductDetail/ProductNameCell.swift
        new file:   ProductDetail/ProductPriceCell.swift
        new file:   ProductDetail/Test/ProductDetailViewModelTests.swift
        new file:   ProductDetail/Test/ProductDetailUseCaseMock.swift
        new file:   ProductDetail/Test/ProductDetailNavigatorMock.swift
        new file:   ProductDetail/Test/ProductDetailViewControllerTests.swift
        new file:   ProductDetail/Test/ProductDetailCellsTests.swift
 
Finish!
```

## 2. Create model from json:

Copy json text to clipboard then using command:

```
$ python it.py json <Model_Name>
```

For example :

Copy json text to clipboard:

```
{
    "id": 989,
    "user_id": 98,
    "content": "Hello world!",
    "type": 9,
    "is_read": false,
    "is_signage": false,
    "created_at": "2018-06-29T17:15:36+09:00",
    "payload": {
        "id": 0,
        "firebase_key": "-LExffRix3JMAk2Kd7D7"
    }
}
```

then using command:
```
$ python it.py json Notice
Text has been copied to clipboard.
```

Clipboard:

```
import ObjectMapper
import Then

struct Payload {
    var id: Int
    var firebaseKey: String
}

extension Payload {
    init() {
        self.init(
            id: 0
            firebaseKey: ""
        )
    }
}

extension Payload: Then, HasID, Hashable { }

extension Payload: Mappable {

    init?(map: Map) {
        self.init()
    }

    mutating func mapping(map: Map) {
        id <- map["id"]
        firebaseKey <- map["firebase_key"]
    }
}

struct Notice {
    var id: Int
    var userId: Int
    var content: String
    var type: Int
    var isRead: Bool
    var isSignage: Bool
    var createdAt: Date
    var payload: Payload?
}

extension Notice {
    init() {
        self.init(
            id: 0
            userId: 0
            content: ""
            type: 0
            isRead: false
            isSignage: false
            createdAt: Date()
        )
    }
}

extension Notice: Then, HasID, Hashable { }

extension Notice: Mappable {

    init?(map: Map) {
        self.init()
    }

    mutating func mapping(map: Map) {
        id <- map["id"]
        userId <- map["user_id"]
        content <- map["content"]
        type <- map["type"]
        isRead <- map["is_read"]
        isSignage <- map["is_signage"]
        createdAt <- (map["created_at"], DateTransform())
        payload <- map["payload"]
    }
}

```
