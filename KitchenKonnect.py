from flet import *
from custom_checkbox import CustomCheckBox
import flet as ft
import mysql.connector
    
def main(page: Page):
    BG = '#BDD1DE'
    FG = '#8AB3CF'
    StrongBlue = '#4180AB'
    WHITE = '#FFFFFF'
    textin = ft.TextField(label="Adicione seu Alimento",
                          width=380,
                          color='WHITE',
                          border_color='WHITE',
                          helper_text='Escreva no Singular.')
    qtdin = ft.TextField(label="Adicione a Quantidade deste Item",
                        width=380,
                        color='WHITE',
                        border_color='WHITE',
                        helper_text='Insira Também a Unidade de Medida (ex: 10Kg)')
    edit_textin = ft.TextField(label="Adicione seu Alimento",
                          width=380,
                          color='WHITE',
                          border_color='WHITE',
                          helper_text='Escreva no Singular.')
    edit_qtdin = ft.TextField(label="Adicione a Quantidade deste Item",
                        width=380,
                        color='WHITE',
                        border_color='WHITE',
                        helper_text='Insira Também a Unidade de Medida (ex: 10Kg)')

    conn = mysql.connector.connect(
      host="127.0.0.1",
      user="root",
      password="root",
      database="KK_mysql"
      )

    cursor = conn.cursor()

    def deletebtn(e):
      print("The id of number ",e.control.data['id'])
      try:
        sql = "DELETE FROM food WHERE id = %s"
        val = (e.control.data['id'],)
        cursor.execute(sql,val)
        conn.commit()
        print (" was successfully deleted")
        mydt.rows.clear()
        load_data()
        page.update()
      except Exception as e:
        print(e)
        print("Unable to delete. Please, get assistance.")
    
    def editdata(e):
      try:
         sql = "UPDATE food SET quantity = %s, nome = %s WHERE nome = %s"
         val = (edit_qtdin.value,edit_textin.value,edit_textin.value)
         cursor.execute(sql,val)
         conn.commit()
         print("Data successfully edited")
         dialog.open = False
         page.update()
         edit_qtdin.value = ""
         edit_textin.value = ""
         mydt.rows.clear()
         load_data()
         page.update()
      except Exception as e:
        print(e)
        print("Unable to edit. Please, get assistance.")
    
    dialog = AlertDialog(
       title=Text("Edit Page"),
       content=Column([
          edit_textin,
          edit_qtdin
       ]),
       actions=[
          TextButton("Save",
                     on_click=editdata
                     )
       ]
    )

    def editbtn(e):
      edit_textin.value = e.control.data['nome']
      edit_qtdin.value = e.control.data['quantity']
      page.dialog = dialog
      dialog.open = True
      page.update() 
    
    mydt = DataTable(
        columns=[
            DataColumn(Text("id")),
            DataColumn(Text("name")),
            DataColumn(Text("amount")),
            DataColumn(Text("actions"))
        ],
        rows=[]
    )

    def load_data():
        #getting data and pushing to datatable
        cursor.execute("SELECT * FROM food")
        result = cursor.fetchall()
        #pushing data to dict
        columns = [column[0] for column in cursor.description]
        rows = [dict(zip(columns,row)) for row in result]
        #loop and push
        for row in rows:
           mydt.rows.append(
               DataRow(
                   cells=[
                       DataCell(Text(row['id'])),
                       DataCell(Text(row['nome'])),
                       DataCell(Text(row['quantity'])),
                       DataCell(
                           Row([
                               IconButton("create",icon_color=StrongBlue,
                                          data=row,
                                          on_click=editbtn
                                          ),
                                IconButton("delete",icon_color=WHITE,
                                          data=row,
                                          on_click=deletebtn
                                          ),
                           ])
                       ),
                   ]
               )
           )
        page.update()

    load_data()

    def handle_on_click(event):
      global input_text
      global input_qtd
      input_text = textin.value
      input_qtd = qtdin.value
      try:
        sql = "INSERT INTO food (nome,quantity) VALUES(%s,%s)"
        val = (input_text,input_qtd)
        cursor.execute(sql,val)
        conn.commit()
        print(cursor.rowcount,"RECORD INSERTED")
        print ("We're Good to Go")
        mydt.rows.clear()
        textin.value = ""
        qtdin.value = ""
        load_data()
        page.update()
      except Exception as e:
            print (e)
            print ("Something wrong is not right")
    
    circle = Stack(
    controls=[
      Container(
        width=100,
        height=100,
        border_radius=50,
        bgcolor='white12'
        ),
      Container(
        gradient=SweepGradient(
          center=alignment.center,
          start_angle=0.0,
          end_angle=3,
          stops=[0.5,0.5],
          colors=['#00000000', StrongBlue],
        ),
        width=100,
        height=100,
        border_radius=50,
        content=Row(alignment='center',
        controls=[
        Container(padding=padding.all(5),
          bgcolor=BG,
          width=90,height=90,
          border_radius=50,
          content=Container(bgcolor=FG,
                    height=80,width=80,
                    border_radius=40,
                    content=CircleAvatar(opacity=0.8,
                      foreground_image_src="/assets/images/2.jpg"
                      )
                  )
        )
        ],
        ),
      ),
    ]
  )
              
    def shrink(e):
      page_2.controls[0].width=120
      page_2.controls[0].scale = transform.Scale(0.8,alignment=alignment.center_right)
      page_2.update()

    def restore(e):
      page_2.controls[0].width=400
      page_2.controls[0].scale = transform.Scale(1,alignment=alignment.center_right)
      page_2.update()

    adding_page = Container(
      content=Column(
        controls=[
            Row(
              alignment='spaceBetween',
              controls=[
                Container(
                  on_click=lambda e:page.go('/'),
                  content=Icon(icons.CLOSE,color=StrongBlue)
                ),
                Row(
                  controls=[
                    Icon(icons.SEARCH,color=StrongBlue),
                    Icon(icons.NOTIFICATIONS_OUTLINED,color=StrongBlue)
                  ]
                )
              ]
            ),
            Container(height=20),
            Text(
              value='ADDING PAGE',size=20,weight='bold',color=WHITE 
            ),
            Container(height=10),
            Container(
              content = textin
            ),
            Container(
              content = qtdin
            ),
            Container(height=20),
            FloatingActionButton(
              icon = icons.ADD,
              on_click=handle_on_click
            ),
            mydt
        ]     
      )
    )

    tasks = Column(
        height=400,
        scroll='auto',
        )
    
    for i in range(10):
        tasks.controls.append(
            Container(height=70,
                      width=400,
                      bgcolor=BG,
                      border_radius=25,
                      padding=padding.only(
                      left=20,top=25),
                      content=CustomCheckBox(
                          color=StrongBlue,
                          label= "data_to_display"
                          ))
        )

    categories_card = Row(scroll='auto')
    categories = ['Comer','Beber','Sobremesa']
    for i, category in enumerate(categories):
        categories_card.controls.append(
            Container(
                bgcolor=BG,
                height=110,
                width=170,
                border_radius=20,
                padding=15,
                content=Column(
                    controls=[
                        Text('## Tasks',color=StrongBlue,weight='bold'),
                        Text(category,color=StrongBlue,weight='bold'),
                        Container(
                            width=160,
                            height=5,
                            bgcolor='white12',
                            border_radius=20,
                            padding=padding.only(right=i*50),
                            content=Container(
                                bgcolor=StrongBlue
                            )
                        )
                    ]
                )
            )
        )

    first_page_contents = Container(
      content=Column(
        controls=[
          Row(
            alignment='spaceBetween',
            controls=[
              Container(
                on_click=lambda e: shrink(e),
                content=Icon(icons.MENU,color=StrongBlue)),
                Row(
                  controls=[
                    Icon(icons.SEARCH,color=StrongBlue),
                    Icon(icons.NOTIFICATIONS_OUTLINED,color=StrongBlue)
                  ]
                )
            ]
          ),
         Container(height=20),
         Text(
           value='What uuuup, <user>!',color=StrongBlue,weight='bold'),
         Text(
           value='CATEGORIAS',size=20,weight='bold'),
         Container(
           padding=padding.only(top=10,bottom=20),
           content=categories_card
         ),
         Container(height=20),
         Text("SEUS ALIMENTOS",size=20,weight='bold'),
         Stack(
             controls=[
                 tasks,
                 FloatingActionButton(
                     bottom=2,right=20,
                     icon = icons.ADD,on_click=lambda _:page.go('/create_task')
                 )
             ]
          )
        ],
      ),
    )
    
    page_1 = Container(
      width=400,
      height=850,
      bgcolor=BG,
      border_radius=35,
      padding=padding.only(left=50,top=60,right=200),
      content=Column(
        controls=[
          Row(alignment='end',
            controls=[
              Container(
                border_radius=25,padding=padding.only(top=13,left=18),
                height=50,width=50,border=border.all(color=StrongBlue,width=1),
                content=Text('<',color=StrongBlue),
                on_click=lambda e: restore(e)
              )
            ]
          ),
          Container(height=20),
          circle,
          Text('User\nUndefined',size=30,weight='bold',color=WHITE),
          Container(height=20),
          Row(
            controls=[
            Icon(icons.FAVORITE_BORDER_SHARP,color=StrongBlue),
            Text('Templates',size=15,weight=FontWeight.W_300,color=StrongBlue)
          ]
          ),
          Container(height=5),
          Row(
            controls=[
            Icon(icons.CATEGORY_OUTLINED,color=StrongBlue),
            Text('Categories',size=15,weight=FontWeight.W_300,color=StrongBlue)
          ]
          ),
          Container(height=5),
          Row(
            controls=[
            Icon(icons.HISTORY_OUTLINED,color=StrongBlue),
            Text('History',size=15,weight=FontWeight.W_300,color=StrongBlue)
          ]
          ),
          Image(src=f"/images/1.png",
          width=300,
          height=200),
          Text('Good',color=WHITE,font_family='poppins',weight='bold'),
          Text('Consistency',size=25,color=StrongBlue,weight='bold')
        ]
      )
    )
    page_2 = Row(alignment='end',
      controls=[
        Container(
          width=400,
          height=850,
          bgcolor=FG,
          border_radius=35,
          animate=animation.Animation(600,AnimationCurve.DECELERATE),
          animate_scale=animation.Animation(400,curve='decelerate'),
          padding=padding.only(
            top=50,left=20,
            right=20,bottom=5
          ),
          content=Column(
            controls=[
              first_page_contents
            ]
          )
        ) 
      ]
    )
    page_3 = Row(
      controls=[
        Container(
          width=400,
          height=850,
          bgcolor=FG,
          border_radius=35,
          animate=animation.Animation(600,AnimationCurve.DECELERATE),
          animate_scale=animation.Animation(400,curve='decelerate'),
          padding=padding.only(
            top=50,left=20,
            right=20,bottom=5
          ),
          content=Column(
            controls=[
              adding_page
            ]
          )
        ) 
      ]
    )

    container = Container(
        width=400,
        height=850,
        bgcolor=BG,
        border_radius=35,
        content=Stack(
            controls=[
                page_1,
                page_2
            ]
            )
    )

    pages = {
        '/':View("/",[container]),
        '/create_task':View("/create_task",[page_3])
    }

    def route_change(route):
        page.views.clear()
        page.views.append(
            pages[page.route]
        )

    page.add(container)

    page.on_route_change = route_change
    page.go(page.route)
    
app(target=main,)