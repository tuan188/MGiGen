# igen - Code Generation Tools for iOS

## Installation:

### Install using pip:

Open Terminal and run:

```
$ pip3 install igen
```

### Update:

```
$ pip3 install -U igen
```

or

```
$ pip3 uninstall igen
$ pip3 install igen --no-cache-dir
```

### Uninstall:

```
$ pip3 uninstall igen
```

## How to install pip3:

pip3 is already installed if you are using Python 3 (>=3.4)

In order to install Python 3, you need to install Homebrew, run the following command in Terminal:

```
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

Then install Python 3:

```
$ brew install python
```

## 1. Create Template:

### 1.1. Base Template:

The Base Template contains the necessary files for a scene in the Clean Architecture pattern.

Open Terminal, navigate to the folder you want to save the files and run:

```
$ igen template base <Scene_Name>
```

The first time you use the template command, you need to enter your project information:

```
Enter project name: Your Project
Enter developer name: Your Name
Enter company name: Your Company
```

Later, if you want to update the information you can run the command:

```
$ igen config project
```

**Example:**

```
$ igen template base Login
```

Output:

```
Successfully created files:
    Login/LoginViewModel.swift
    Login/LoginNavigator.swift
    Login/LoginUseCase.swift
    Login/LoginViewController.swift
    Login/LoginAssembler.swift
    Login/Test/LoginViewModelTests.swift
    Login/Test/LoginUseCaseMock.swift
    Login/Test/LoginNavigatorMock.swift
    Login/Test/LoginViewControllerTests.swift
```

### 1.2. List Template:

The List Template shows a list of items in the UITableView or UICollectionView.

Copy the model to the pasteboard (clipboard) then run the command:

```
$ igen template list <Scene_Name> [--section] [--collection]
```

**Options**:

`--section`: show a list of items with header sections.

`--collection`: use UICollectionView instead of UITableView

**Example:**

Copy the following text to the pasteboard:

``` Swift
struct Product {
    let id: Int
    let name: String
    let price: Double
}
```

then run the command:

```
$ igen template list ProductList
```

Output:

```
Successfully created files:
    ProductList/ProductListViewModel.swift
    ProductList/ProductViewModel.swift
    ProductList/ProductListNavigator.swift
    ProductList/ProductListUseCase.swift
    ProductList/ProductListViewController.swift
    ProductList/ProductCell.swift
    ProductList/ProductListAssembler.swift
    ProductList/Test/ProductListViewModelTests.swift
    ProductList/Test/ProductListUseCaseMock.swift
    ProductList/Test/ProductListNavigatorMock.swift
    ProductList/Test/ProductListViewControllerTests.swift
    ProductList/Test/ProductCellTests.swift
```

### 1.3. Detail Template:

The Detail Template shows item details in a UITableView.

Copy the model to the pasteboard then run the command:

```
$ igen template detail <Scene_Name> [--static]
```

**Options**:

`--static`: display item detail in a static UITableViewController.

**Example:**

Copy the following text to the pasteboard:

``` Swift
struct Product {
    let id: Int
    let name: String
    let price: Double
}
```

then run the command:

```
$ igen template detail ProductDetail
```
 
Output:

```
Successfully created files:
    ProductDetail/ProductDetailViewModel.swift
    ProductDetail/ProductDetailNavigator.swift
    ProductDetail/ProductDetailUseCase.swift
    ProductDetail/ProductDetailViewController.swift
    ProductDetail/ProductIdCell.swift
    ProductDetail/ProductNameCell.swift
    ProductDetail/ProductPriceCell.swift
    ProductDetail/ProductDetailAssembler.swift
    ProductDetail/Test/ProductDetailViewModelTests.swift
    ProductDetail/Test/ProductDetailUseCaseMock.swift
    ProductDetail/Test/ProductDetailNavigatorMock.swift
    ProductDetail/Test/ProductDetailViewControllerTests.swift
    ProductDetail/Test/ProductDetailCellsTests.swift
```

## 2. Create mock for protocol:

Copy the protocol to the pasteboard then run the command:

```
$ igen mock [-p]
```

**Options**:

`-p`, `--print`: print the result.

**Example**:

Copy the following text to the pasteboard:

``` Swift
protocol ProductsNavigatorType {
    func toProducts()
    func toProductDetail(product: Product)
    func toEditProduct(_ product: Product) -> Driver<EditProductDelegate>
}
```

then run the command:

```
$ igen mock
```

Output:

```
The result has been copied to the pasteboard.
```

Content in the pasteboard:

``` Swift
final class ProductsNavigatorMock: ProductsNavigatorType {
    // MARK: - toProducts
    var toProducts_Called = false
    func toProducts() {
        toProducts_Called = true
    }
    
    // MARK: - toProductDetail
    var toProductDetail_Called = false
    func toProductDetail(product: Product) {
        toProductDetail_Called = true
    }
    
    // MARK: - toEditProduct
    var toEditProduct_Called = false
    var toEditProduct_ReturnValue: Driver<EditProductDelegate> = Driver.empty()
    func toEditProduct(_ product: Product) -> Driver<EditProductDelegate> {
        toEditProduct_Called = true
        return toEditProduct_ReturnValue
    }
    
}
```

## 3. Create unit tests for view model:

Copy the view model to the pasteboard then run the command:

```
$ igen test [-p]
```

**Options**:

`-p`, `--print`: print the result.

**Example**:

Copy the following text to the pasteboard:

``` Swift
struct AppViewModel: ViewModelType {

    struct Input {
        let loadTrigger: Driver<Void>
    }

    struct Output {
        let toMain: Driver<Void>
    }
```

then run the command:

```
$ igen test
```

Output:

```
The result has been copied to the pasteboard.
```

Content in the pasteboard:

``` Swift
final class AppViewModelTests: XCTestCase {
    private var viewModel: AppViewModel!
    private var navigator: AppNavigatorMock!
    private var useCase: AppUseCaseMock!
    private var disposeBag: DisposeBag!
    private var input: AppViewModel.Input!
    private var output: AppViewModel.Output!
    private let loadTrigger = PublishSubject<Void>()

    override func setUp() {
        super.setUp()
        navigator = AppNavigatorMock()
        useCase = AppUseCaseMock()
        viewModel = AppViewModel(navigator: navigator, useCase: useCase)
        disposeBag = DisposeBag()

        input = AppViewModel.Input(
            loadTrigger: loadTrigger.asDriverOnErrorJustComplete()
        )
        output = viewModel.transform(input)
        output.toMain.drive().disposed(by: disposeBag)
    }
    
    func test_loadTrigger_() {
        // arrange


        // act


        // assert
        XCTAssert(true)
    }

}
```

## 4. Create init method for model:

Copy the model to the pasteboard then run the command:

```
$ igen init [-p]
```

**Options**:

`-p`, `--print`: print the result.

**Example**:

Copy the following text to the pasteboard:

``` Swift
struct Product {
    var id: Int
    var name: String
    var price: Double
}
```

then run the command:

```
$ igen init
```

Output:

```
The result has been copied to the pasteboard.
```

Content in the pasteboard:

``` Swift
extension Product {
    init() {
        self.init(
            id: 0,
            name: "",
            price: 0.0
        )
    }
}
```

## 5. Create model from json:

Copy the json to the pasteboard then run the command:

```
$ igen json <Model_Name> [-p]
```

**Options**:

`-p`, `--print`: print the result.

**Example**:

Copy the following text to the pasteboard:

``` JSON
{
    "id": 989,
    "content": "Hello world!",
    "is_read": false,
    "created_at": "2018-06-29T17:15:36+09:00"
}
```

then run the command:

```
$ igen json Notice
```

Output:

```
The result has been copied to the pasteboard.
```

Content in the pasteboard:

``` Swift
struct Notice {
    var id: Int
    var content: String
    var isRead: Bool
    var createdAt: Date
}

extension Notice {
    init() {
        self.init(
            id: 0,
            content: "",
            isRead: false,
            createdAt: Date()
        )
    }
}

extension Notice: Then { }

extension Notice: Mappable {
    init?(map: Map) {
        self.init()
    }

    mutating func mapping(map: Map) {
        id <- map["id"]
        content <- map["content"]
        isRead <- map["is_read"]
        createdAt <- (map["created_at"], DateTransform())
    }
}
```

## 6. Other commands:

See:
```
igen -h
```






