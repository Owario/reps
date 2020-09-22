Техническое задание на разработку программного обеспечения баз данных.


4. Назначение и цели создания системы:

4.1. Назначение разработки:

Каталог художественной литературы. 

4.2. Цели создания:

Упрощение процесса выбора книги для чтения, возможность получать информацию о популярных книгах в рамках определённых жанров, а также книг, которые заинтересовали других пользователей; возможность читать отзывы и тем самым получать представление о той или иной книге.


12. Разработка проекта системы базы данных:

12.1. Требования к составу данных:

(возможны изменения)

Учётные записи пользователей: имя (уникальное), пароль (желательно в хэшированном виде), информация "о себе" (при создании страницы - null) - строковый формат, модераторство - логическое значение (при регистрации автоматически ложь, изменяется вручную администратором с помощью специальной формы на странице пользователя (которая видна также только администратору)), первичный ключ;
“учётные записи” книг - автор (единственный), название, жанр, - строковый формат, рейтинг - числовой формат, первичный ключ; 
комментарии - тело комментария, автор комментария, название комментируемой книги - текстовый формат, первичный ключ; 
отношения: “пользователь-книга”, “пользователь-комментарий”, “книга-комментарий”.


12.2. Требования к представлению информации:

Информация должна предоставляться пользователям ресурса посредством приложения, работающего на операционной системе windows, имеющего следующие основные разделы: 
“страница” пользователя для каждого пользователя ресурса, “страница” книги для каждой книги каталога, - с информацией, отображаемой в текстовом формате; 
каталог книг, а также страницы выдачи информации при поиске. 
В случае большого объёма предоставляемой информации должно предполагаться разделение информации на несколько страниц, с возможностью перейти на соседние страницы с помощью кнопок. 
Каталог представляет собой отдельный раздел сайта, информация на котором разделена на страницы для удобства просмотра. В этом разделе представлены ссылки на страницы книг, отсортированные по рейтингу, с возможностью просмотреть только книги определённого жанра, а также отдельное поле для ввода информации для поиска. Такой информацией может быть имя пользователя, фамилия автора книги, название книги. Предварительно пользователю необходимо уточнить (во всплывающем окне(?)), информацию какого рода он планирует искать. Результатом поиска является страница, на которой, в случае успешного поиска, находится ссылка на страницу пользователя/книги либо несколько ссылок на страницы книг искомого автора (в случае поиска по фамилии автора), отсортированные по рейтингу; в случае неуспешного поиска предоставляется сообщение в текстовом формате о невозможности нахождения данной информации.
Страница книги представляет собой отображение информации о книге (автор, название, жанр), ссылки на страницу, на которой будут отображены все книги данного автора, с сортировкой по рейтингу и разделением по страницам; комментарии других пользователей о данной книге со ссылками на страницы соответствующих авторов и разделением по страницам.
Страница пользователя представляет собой отображение основной информации о пользователе - имени пользователя, информации "о себе"; а также комментариев, написанных пользователем со ссылками на страницы соответствующих книг и разделением по страницам. При просмотре страницы пользователя доступны для просмотра списки "читал", "хочу читать", "читаю" - страницы со ссылками на страницы соответствующих книг.
Зарегистрированный пользователь может добавлять книги из общей базы в свой список с разными метками: читал, читаю, хочу прочитать. 
Книгу можно оценить по 10-балльной шкале (факт оценки будет виден на личной странице пользователя).
К книге можно оставить комментарий-отзыв, который будет виден на странице книги и на личной странице пользователя. 
Незарегистрированный пользователь может листать каталог, читать комментарии, переходить на личные страницы зарегистрированных пользователей.


12.3. Требования по применению СУБД:

База данных необходима для сохранения в долговременной памяти информации об экземплярах каталога книг, комментариев пользователей и данных учётных записей пользователей, а также связей между этими сущностями; а также для сохранения в долговременной памяти новой информации при добавлении её пользователями и/или администраторами ресурса. Требуется реляционная база данных, т.к. при предоставлении информации необходимо учитывать связи между сущностями.

13.Заполнение базы данных информацией:

13.1. Требования к заполнению базы данных:

Пользователь заполняет собственную страницу при регистрации, в дальнейшем может изменять некоторые поля. 
Пользователь может писать комментарии к книгам, редактировать свои комментарии, удалять их. 
Пользователь может ставить оценку к книге и изменять её. 
Пользователь может добавлять книгу в разделы: читал, читаю, хочу прочитать, без раздела. 
Модератор может добавлять новые книги, редактировать информацию к книгам, удалять комментарии пользователей. 
Информация о личной странице пользователя - текстовый формат. Информация о книгах - текстовый формат. Комментарии пользователей - текстовый формат.

13.2. Требования к источникам информации:

Пользователи ресурса (для заполнения личных страниц и написания комментариев). 
Всемирная сеть интернет и всё, что касается мировой библиотеки (для заполнения каталога). 


Состав команды:

Горбань Егор (331), Салихов Марат (331).
