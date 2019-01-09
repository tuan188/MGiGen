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
The Base Template contains necessary files for a scene in the [Clean Architecture](https://github.com/tuan188/MGCleanArchitecture) pattern.

Open Terminal, navigate to the folder you want to save the files and run:

```
$ igen template base <Scene_Name>
```

The first time you use the `template` command, you need to enter your project information:

```
Enter project name: Your Project
Enter developer name: Your Name
Enter company name: Your Company
```

Later, if you want to update the information you can run the command:

```
$ igen config project
```

#### Example:

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
The List Template shows a list of objects in the UITableView or UICollectionView.

Copy the model to the pasteboard (clipboard) then run the command:

```
$ igen template list <Scene_Name> [--section] [--collection]
```

#### Options:

`--section`: show the list with header sections.

`--collection`: use UICollectionView instead of UITableView

#### Example:
Copy the following text to the pasteboard:

```swift
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
The Detail Template shows details of a object in a UITableView.

Copy the model to the pasteboard then run the command:

```
$ igen template detail <Scene_Name> [--static]
```

#### Options:

`--static`: display details of the object in a static UITableViewController.

#### Example:
Copy the following text to the pasteboard:

```swift
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

### 1.4. Skeleton Template:
To create a Clean Architecture skeleton project, run:

```
$ igen template skeleton <Folder_Name>
```

#### Example:
Run the following command in Terminal:

```
$ igen template skeleton DemoApp
```

Output:

```
Successfully created files:
    DemoApp/Podfile
    DemoApp/Localizable.strings
    DemoApp/swiftlint.yml
    DemoApp/UnitTestViewController.swift
    DemoApp/AppDelegate.swift
    DemoApp/Medical-Bridging-Header.h
    DemoApp/Assembler/Assembler.swift
    DemoApp/Support/Utils.swift
    DemoApp/Extensions/UIViewController+.swift
    DemoApp/Extensions/UIViewController+Rx.swift
    DemoApp/Platform/Services/API/APIError.swift
    DemoApp/Platform/Services/API/APIService.swift
    DemoApp/Platform/Services/API/APIInput.swift
    DemoApp/Platform/Services/API/APIOutput.swift
    DemoApp/Platform/Services/API/APIUrls.swift
    DemoApp/Scenes/App/AppAssembler.swift
    DemoApp/Scenes/App/AppNavigator.swift
    DemoApp/Scenes/App/AppUseCase.swift
    DemoApp/Scenes/App/AppViewModel.swift
    DemoApp/Scenes/Storyboards/Storyboards.swift
```

### 1.5. Form Input Template:
To create a form input template for a model, copy the model then run the command:

```
$ igen template form <Scene_Name> [--submit SUBMIT]
```

#### Options:

`--submit`: set the name of the submit action.

#### Example:
Copy the following text to the pasteboard:

```swift
struct Product {
    let name: String
    let price: Double
}
```

then run the command:

```
$ igen template form CreateProduct --submit Create
```

Output:

```
Successfully created files:
    CreateProduct/CreateProductAssembler.swift
    CreateProduct/CreateProductNavigator.swift
    CreateProduct/CreateProductViewModel.swift
    CreateProduct/CreateProductUseCase.swift
    CreateProduct/CreateProductViewController.swift
    CreateProduct/Test/CreateProductUseCaseMock.swift
    CreateProduct/Test/CreateProductNavigatorMock.swift
    CreateProduct/Test/CreateProductViewModelTests.swift
    CreateProduct/Test/CreateProductViewControllerTests.swift
```

## 2. Create a mock class for a protocol/function:
Copy the protocol/function to the pasteboard then run the command:

```
$ igen mock [-p]
```

#### Options:

`-p`, `--print`: print the result.

#### Example:
Copy the following text to the pasteboard:

```swift
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

```swift
final class ProductsNavigatorMock: ProductsNavigatorType {
    
    // MARK: - toProducts
    
    var toProductsCalled = false

    func toProducts() {
        toProductsCalled = true
    } 

    // MARK: - toProductDetail
    
    var toProductDetailCalled = false

    func toProductDetail(product: Product) {
        toProductDetailCalled = true
    } 

    // MARK: - toEditProduct
    
    var toEditProductCalled = false
    var toEditProductReturnValue: Driver<EditProductDelegate> = Driver.empty()

    func toEditProduct(_ product: Product) -> Driver<EditProductDelegate> {
        toEditProductCalled = true
        return toEditProductReturnValue
    } 
}
```

## 3. Create unit tests for a view model:
Copy the view model to the pasteboard then run the command:

```
$ igen test [-p]
```

#### Options:

`-p`, `--print`: print the result.

#### Example:

Copy the following text to the pasteboard:

```swift
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

```swift
final class AppViewModelTests: XCTestCase {
    private var viewModel: AppViewModel!
    private var navigator: AppNavigatorMock!
    private var useCase: AppUseCaseMock!
    
    private var input: AppViewModel.Input!
    private var output: AppViewModel.Output!

    private var disposeBag: DisposeBag!

    private let loadTrigger = PublishSubject<Void>()

    override func setUp() {
        super.setUp()
        navigator = AppNavigatorMock()
        useCase = AppUseCaseMock()
        viewModel = AppViewModel(navigator: navigator, useCase: useCase)
        
        input = AppViewModel.Input(
            loadTrigger: loadTrigger.asDriverOnErrorJustComplete()
        )

        output = viewModel.transform(input)

        disposeBag = DisposeBag()

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

## 4. Create a initialize method for a class/struct:
Copy the class/struct to the pasteboard then run the command:

```
$ igen init [-p]
```

#### Options:

`-p`, `--print`: print the result.

#### Example:

Copy the following text to the pasteboard:

```swift
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

```swift
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

## 5. Create models from JSON:
Copy the json to the pasteboard then run the command:

```
$ igen json <Model_Name> [-p]
```

#### Options:

`—return-classes`: return classes instead of structs.

`-p`, `--print`: print the result.

#### Example:
Copy the following text to the pasteboard:

```json
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

```swift
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

## 6. Configuration:
### 6.1. Configure the project information:
To update the project information, run the command:

```
$ igen config project
```

If you want to update the project name only, run the command:

```
$ igen config project.name <Project_Name>
```

or update the developer name:

```
$ igen config project.developer <Developer_Name>
```

or update the company name:

```
$ igen config project.company <Company_Name>
```

### 6.2. View the project information:
To view the project information, run the command:

```
$ igen config project -i
```

## 7. Other commands:
Run:

```
$ igen -h
```
