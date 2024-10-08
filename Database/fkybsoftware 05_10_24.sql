PGDMP      ,            	    |            fkybsoftware    16.3    16.3 }    �           0    0    ENCODING    ENCODING        SET client_encoding = 'UTF8';
                      false            �           0    0 
   STDSTRINGS 
   STDSTRINGS     (   SET standard_conforming_strings = 'on';
                      false            �           0    0 
   SEARCHPATH 
   SEARCHPATH     8   SELECT pg_catalog.set_config('search_path', '', false);
                      false            �           1262    17080    fkybsoftware    DATABASE     n   CREATE DATABASE fkybsoftware WITH TEMPLATE = template0 ENCODING = 'UTF8' LOCALE_PROVIDER = libc LOCALE = 'C';
    DROP DATABASE fkybsoftware;
                postgres    false                        2615    2200    public    SCHEMA        CREATE SCHEMA public;
    DROP SCHEMA public;
                pg_database_owner    false            �           0    0    SCHEMA public    COMMENT     6   COMMENT ON SCHEMA public IS 'standard public schema';
                   pg_database_owner    false    4            �            1259    17098 	   categoria    TABLE     q   CREATE TABLE public.categoria (
    id_categoria integer NOT NULL,
    nombre character varying(255) NOT NULL
);
    DROP TABLE public.categoria;
       public         heap    postgres    false    4            �            1259    17097    categoria_id_categoria_seq    SEQUENCE     �   CREATE SEQUENCE public.categoria_id_categoria_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.categoria_id_categoria_seq;
       public          postgres    false    4    220            �           0    0    categoria_id_categoria_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.categoria_id_categoria_seq OWNED BY public.categoria.id_categoria;
          public          postgres    false    219            �            1259    17105    cliente    TABLE     �  CREATE TABLE public.cliente (
    id_cliente integer NOT NULL,
    nombre_completo character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    fecha date NOT NULL,
    metodo_pago character varying(20) NOT NULL,
    notas character varying(255) NOT NULL,
    descripcion character varying(255) NOT NULL,
    condicion_venta character varying(15) NOT NULL,
    id_direccion integer
);
    DROP TABLE public.cliente;
       public         heap    postgres    false    4            �            1259    17104    cliente_id_cliente_seq    SEQUENCE     �   CREATE SEQUENCE public.cliente_id_cliente_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.cliente_id_cliente_seq;
       public          postgres    false    222    4            �           0    0    cliente_id_cliente_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.cliente_id_cliente_seq OWNED BY public.cliente.id_cliente;
          public          postgres    false    221            �            1259    17185 	   conductor    TABLE     �   CREATE TABLE public.conductor (
    id_conductor integer NOT NULL,
    nombre character varying(255) NOT NULL,
    apellidos character varying(255) NOT NULL,
    identificacion character varying(255) NOT NULL,
    placa character varying(20) NOT NULL
);
    DROP TABLE public.conductor;
       public         heap    postgres    false    4            �            1259    17184    conductor_id_conductor_seq    SEQUENCE     �   CREATE SEQUENCE public.conductor_id_conductor_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.conductor_id_conductor_seq;
       public          postgres    false    4    242            �           0    0    conductor_id_conductor_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.conductor_id_conductor_seq OWNED BY public.conductor.id_conductor;
          public          postgres    false    241            �            1259    17146    detalle_factura    TABLE     �   CREATE TABLE public.detalle_factura (
    id_detalle_factura integer NOT NULL,
    cantidad integer NOT NULL,
    total numeric(10,2) NOT NULL,
    id_producto integer,
    id_factura integer
);
 #   DROP TABLE public.detalle_factura;
       public         heap    postgres    false    4            �            1259    17145 &   detalle_factura_id_detalle_factura_seq    SEQUENCE     �   CREATE SEQUENCE public.detalle_factura_id_detalle_factura_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 =   DROP SEQUENCE public.detalle_factura_id_detalle_factura_seq;
       public          postgres    false    232    4            �           0    0 &   detalle_factura_id_detalle_factura_seq    SEQUENCE OWNED BY     q   ALTER SEQUENCE public.detalle_factura_id_detalle_factura_seq OWNED BY public.detalle_factura.id_detalle_factura;
          public          postgres    false    231            �            1259    17162 	   direccion    TABLE       CREATE TABLE public.direccion (
    id_direccion integer NOT NULL,
    provincia character varying(255) NOT NULL,
    canton character varying(255) NOT NULL,
    distrito character varying(255) NOT NULL,
    direccion_exacta character varying(255) NOT NULL
);
    DROP TABLE public.direccion;
       public         heap    postgres    false    4            �            1259    17161    direccion_id_direccion_seq    SEQUENCE     �   CREATE SEQUENCE public.direccion_id_direccion_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.direccion_id_direccion_seq;
       public          postgres    false    236    4            �           0    0    direccion_id_direccion_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.direccion_id_direccion_seq OWNED BY public.direccion.id_direccion;
          public          postgres    false    235            �            1259    17114    factura    TABLE     y  CREATE TABLE public.factura (
    id_factura integer NOT NULL,
    moneda character varying(255),
    metodo_pago character varying(20) NOT NULL,
    fecha date NOT NULL,
    total numeric(10,2) NOT NULL,
    tipo_pago character varying(255) NOT NULL,
    estado character varying(15) NOT NULL,
    id_cliente integer NOT NULL,
    id_direccion integer,
    id_ruta integer
);
    DROP TABLE public.factura;
       public         heap    postgres    false    4            �            1259    17113    factura_id_factura_seq    SEQUENCE     �   CREATE SEQUENCE public.factura_id_factura_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.factura_id_factura_seq;
       public          postgres    false    4    224            �           0    0    factura_id_factura_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.factura_id_factura_seq OWNED BY public.factura.id_factura;
          public          postgres    false    223            �            1259    17137    factura_proveedor    TABLE       CREATE TABLE public.factura_proveedor (
    id_factura_proveedor integer NOT NULL,
    descripcion character varying(255),
    subtotal numeric(10,2) NOT NULL,
    impuesto numeric(10,2) NOT NULL,
    descuento numeric(10,2) NOT NULL,
    total numeric(10,2) NOT NULL,
    estado character varying(15) NOT NULL,
    fecha_entrega date,
    lugar_entrega character varying(255),
    metodo_pago character varying(50),
    notas_adicionales character varying(255),
    id_proveedor integer NOT NULL,
    id_usuario integer
);
 %   DROP TABLE public.factura_proveedor;
       public         heap    postgres    false    4            �            1259    17136 *   factura_proveedor_id_factura_proveedor_seq    SEQUENCE     �   CREATE SEQUENCE public.factura_proveedor_id_factura_proveedor_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 A   DROP SEQUENCE public.factura_proveedor_id_factura_proveedor_seq;
       public          postgres    false    230    4            �           0    0 *   factura_proveedor_id_factura_proveedor_seq    SEQUENCE OWNED BY     y   ALTER SEQUENCE public.factura_proveedor_id_factura_proveedor_seq OWNED BY public.factura_proveedor.id_factura_proveedor;
          public          postgres    false    229            �            1259    17123 
   inventario    TABLE     �   CREATE TABLE public.inventario (
    id_inventario integer NOT NULL,
    estado character varying(255) NOT NULL,
    cantidad integer NOT NULL,
    precio numeric(10,2) NOT NULL,
    id_producto integer
);
    DROP TABLE public.inventario;
       public         heap    postgres    false    4            �            1259    17122    inventario_id_inventario_seq    SEQUENCE     �   CREATE SEQUENCE public.inventario_id_inventario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public.inventario_id_inventario_seq;
       public          postgres    false    226    4            �           0    0    inventario_id_inventario_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE public.inventario_id_inventario_seq OWNED BY public.inventario.id_inventario;
          public          postgres    false    225            �            1259    17130 
   orden_item    TABLE     �   CREATE TABLE public.orden_item (
    id_orden_item integer NOT NULL,
    cantidad integer NOT NULL,
    precio_unidad numeric(10,2) NOT NULL,
    id_factura_proveedor integer,
    id_producto integer
);
    DROP TABLE public.orden_item;
       public         heap    postgres    false    4            �            1259    17129    orden_item_id_orden_item_seq    SEQUENCE     �   CREATE SEQUENCE public.orden_item_id_orden_item_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public.orden_item_id_orden_item_seq;
       public          postgres    false    4    228            �           0    0    orden_item_id_orden_item_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE public.orden_item_id_orden_item_seq OWNED BY public.orden_item.id_orden_item;
          public          postgres    false    227            �            1259    17082    producto    TABLE       CREATE TABLE public.producto (
    id_producto integer NOT NULL,
    descripcion character varying(255),
    unidad_medida integer NOT NULL,
    cantidad integer NOT NULL,
    moneda character varying(20) NOT NULL,
    precio_costo integer,
    id_categoria integer
);
    DROP TABLE public.producto;
       public         heap    postgres    false    4            �            1259    17081    producto_id_producto_seq    SEQUENCE     �   CREATE SEQUENCE public.producto_id_producto_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 /   DROP SEQUENCE public.producto_id_producto_seq;
       public          postgres    false    4    216            �           0    0    producto_id_producto_seq    SEQUENCE OWNED BY     U   ALTER SEQUENCE public.producto_id_producto_seq OWNED BY public.producto.id_producto;
          public          postgres    false    215            �            1259    17089 	   proveedor    TABLE     �  CREATE TABLE public.proveedor (
    id_proveedor integer NOT NULL,
    nombre_completo character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    fecha_ingreso date NOT NULL,
    nombre_de_la_empresa character varying(20) NOT NULL,
    tipo_identificacion character varying(255) NOT NULL,
    identificacion character varying(255) NOT NULL,
    telefono1 character varying(15) NOT NULL,
    telefono2 character varying(15),
    id_direccion integer
);
    DROP TABLE public.proveedor;
       public         heap    postgres    false    4            �            1259    17088    proveedor_id_proveedor_seq    SEQUENCE     �   CREATE SEQUENCE public.proveedor_id_proveedor_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 1   DROP SEQUENCE public.proveedor_id_proveedor_seq;
       public          postgres    false    218    4            �           0    0    proveedor_id_proveedor_seq    SEQUENCE OWNED BY     Y   ALTER SEQUENCE public.proveedor_id_proveedor_seq OWNED BY public.proveedor.id_proveedor;
          public          postgres    false    217            �            1259    17171    ruta    TABLE     p   CREATE TABLE public.ruta (
    id_ruta integer NOT NULL,
    id_transporte integer,
    id_conductor integer
);
    DROP TABLE public.ruta;
       public         heap    postgres    false    4            �            1259    17253    ruta_direccion    TABLE     h   CREATE TABLE public.ruta_direccion (
    id_ruta integer NOT NULL,
    id_direccion integer NOT NULL
);
 "   DROP TABLE public.ruta_direccion;
       public         heap    postgres    false    4            �            1259    17170    ruta_id_ruta_seq    SEQUENCE     �   CREATE SEQUENCE public.ruta_id_ruta_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 '   DROP SEQUENCE public.ruta_id_ruta_seq;
       public          postgres    false    4    238            �           0    0    ruta_id_ruta_seq    SEQUENCE OWNED BY     E   ALTER SEQUENCE public.ruta_id_ruta_seq OWNED BY public.ruta.id_ruta;
          public          postgres    false    237            �            1259    17178 
   transporte    TABLE     a   CREATE TABLE public.transporte (
    id_transporte integer NOT NULL,
    id_conductor integer
);
    DROP TABLE public.transporte;
       public         heap    postgres    false    4            �            1259    17177    transporte_id_transporte_seq    SEQUENCE     �   CREATE SEQUENCE public.transporte_id_transporte_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 3   DROP SEQUENCE public.transporte_id_transporte_seq;
       public          postgres    false    4    240            �           0    0    transporte_id_transporte_seq    SEQUENCE OWNED BY     ]   ALTER SEQUENCE public.transporte_id_transporte_seq OWNED BY public.transporte.id_transporte;
          public          postgres    false    239            �            1259    17153    usuario    TABLE     �   CREATE TABLE public.usuario (
    id_usuario integer NOT NULL,
    nombre_completo character varying(255) NOT NULL,
    email character varying(255) NOT NULL,
    fecha date NOT NULL
);
    DROP TABLE public.usuario;
       public         heap    postgres    false    4            �            1259    17152    usuario_id_usuario_seq    SEQUENCE     �   CREATE SEQUENCE public.usuario_id_usuario_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
 -   DROP SEQUENCE public.usuario_id_usuario_seq;
       public          postgres    false    4    234            �           0    0    usuario_id_usuario_seq    SEQUENCE OWNED BY     Q   ALTER SEQUENCE public.usuario_id_usuario_seq OWNED BY public.usuario.id_usuario;
          public          postgres    false    233            �           2604    17101    categoria id_categoria    DEFAULT     �   ALTER TABLE ONLY public.categoria ALTER COLUMN id_categoria SET DEFAULT nextval('public.categoria_id_categoria_seq'::regclass);
 E   ALTER TABLE public.categoria ALTER COLUMN id_categoria DROP DEFAULT;
       public          postgres    false    219    220    220            �           2604    17108    cliente id_cliente    DEFAULT     x   ALTER TABLE ONLY public.cliente ALTER COLUMN id_cliente SET DEFAULT nextval('public.cliente_id_cliente_seq'::regclass);
 A   ALTER TABLE public.cliente ALTER COLUMN id_cliente DROP DEFAULT;
       public          postgres    false    222    221    222            �           2604    17188    conductor id_conductor    DEFAULT     �   ALTER TABLE ONLY public.conductor ALTER COLUMN id_conductor SET DEFAULT nextval('public.conductor_id_conductor_seq'::regclass);
 E   ALTER TABLE public.conductor ALTER COLUMN id_conductor DROP DEFAULT;
       public          postgres    false    242    241    242            �           2604    17149 "   detalle_factura id_detalle_factura    DEFAULT     �   ALTER TABLE ONLY public.detalle_factura ALTER COLUMN id_detalle_factura SET DEFAULT nextval('public.detalle_factura_id_detalle_factura_seq'::regclass);
 Q   ALTER TABLE public.detalle_factura ALTER COLUMN id_detalle_factura DROP DEFAULT;
       public          postgres    false    232    231    232            �           2604    17165    direccion id_direccion    DEFAULT     �   ALTER TABLE ONLY public.direccion ALTER COLUMN id_direccion SET DEFAULT nextval('public.direccion_id_direccion_seq'::regclass);
 E   ALTER TABLE public.direccion ALTER COLUMN id_direccion DROP DEFAULT;
       public          postgres    false    236    235    236            �           2604    17117    factura id_factura    DEFAULT     x   ALTER TABLE ONLY public.factura ALTER COLUMN id_factura SET DEFAULT nextval('public.factura_id_factura_seq'::regclass);
 A   ALTER TABLE public.factura ALTER COLUMN id_factura DROP DEFAULT;
       public          postgres    false    223    224    224            �           2604    17140 &   factura_proveedor id_factura_proveedor    DEFAULT     �   ALTER TABLE ONLY public.factura_proveedor ALTER COLUMN id_factura_proveedor SET DEFAULT nextval('public.factura_proveedor_id_factura_proveedor_seq'::regclass);
 U   ALTER TABLE public.factura_proveedor ALTER COLUMN id_factura_proveedor DROP DEFAULT;
       public          postgres    false    229    230    230            �           2604    17126    inventario id_inventario    DEFAULT     �   ALTER TABLE ONLY public.inventario ALTER COLUMN id_inventario SET DEFAULT nextval('public.inventario_id_inventario_seq'::regclass);
 G   ALTER TABLE public.inventario ALTER COLUMN id_inventario DROP DEFAULT;
       public          postgres    false    226    225    226            �           2604    17133    orden_item id_orden_item    DEFAULT     �   ALTER TABLE ONLY public.orden_item ALTER COLUMN id_orden_item SET DEFAULT nextval('public.orden_item_id_orden_item_seq'::regclass);
 G   ALTER TABLE public.orden_item ALTER COLUMN id_orden_item DROP DEFAULT;
       public          postgres    false    227    228    228            �           2604    17085    producto id_producto    DEFAULT     |   ALTER TABLE ONLY public.producto ALTER COLUMN id_producto SET DEFAULT nextval('public.producto_id_producto_seq'::regclass);
 C   ALTER TABLE public.producto ALTER COLUMN id_producto DROP DEFAULT;
       public          postgres    false    215    216    216            �           2604    17092    proveedor id_proveedor    DEFAULT     �   ALTER TABLE ONLY public.proveedor ALTER COLUMN id_proveedor SET DEFAULT nextval('public.proveedor_id_proveedor_seq'::regclass);
 E   ALTER TABLE public.proveedor ALTER COLUMN id_proveedor DROP DEFAULT;
       public          postgres    false    218    217    218            �           2604    17174    ruta id_ruta    DEFAULT     l   ALTER TABLE ONLY public.ruta ALTER COLUMN id_ruta SET DEFAULT nextval('public.ruta_id_ruta_seq'::regclass);
 ;   ALTER TABLE public.ruta ALTER COLUMN id_ruta DROP DEFAULT;
       public          postgres    false    238    237    238            �           2604    17181    transporte id_transporte    DEFAULT     �   ALTER TABLE ONLY public.transporte ALTER COLUMN id_transporte SET DEFAULT nextval('public.transporte_id_transporte_seq'::regclass);
 G   ALTER TABLE public.transporte ALTER COLUMN id_transporte DROP DEFAULT;
       public          postgres    false    239    240    240            �           2604    17156    usuario id_usuario    DEFAULT     x   ALTER TABLE ONLY public.usuario ALTER COLUMN id_usuario SET DEFAULT nextval('public.usuario_id_usuario_seq'::regclass);
 A   ALTER TABLE public.usuario ALTER COLUMN id_usuario DROP DEFAULT;
       public          postgres    false    233    234    234            �          0    17098 	   categoria 
   TABLE DATA                 public          postgres    false    220   �       �          0    17105    cliente 
   TABLE DATA                 public          postgres    false    222   -�       �          0    17185 	   conductor 
   TABLE DATA                 public          postgres    false    242   G�       �          0    17146    detalle_factura 
   TABLE DATA                 public          postgres    false    232   a�       �          0    17162 	   direccion 
   TABLE DATA                 public          postgres    false    236   {�       �          0    17114    factura 
   TABLE DATA                 public          postgres    false    224   ��       �          0    17137    factura_proveedor 
   TABLE DATA                 public          postgres    false    230   ��       �          0    17123 
   inventario 
   TABLE DATA                 public          postgres    false    226   ɗ       �          0    17130 
   orden_item 
   TABLE DATA                 public          postgres    false    228   �       �          0    17082    producto 
   TABLE DATA                 public          postgres    false    216   ��       �          0    17089 	   proveedor 
   TABLE DATA                 public          postgres    false    218   �       �          0    17171    ruta 
   TABLE DATA                 public          postgres    false    238   1�       �          0    17253    ruta_direccion 
   TABLE DATA                 public          postgres    false    243   K�       �          0    17178 
   transporte 
   TABLE DATA                 public          postgres    false    240   e�       �          0    17153    usuario 
   TABLE DATA                 public          postgres    false    234   �       �           0    0    categoria_id_categoria_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.categoria_id_categoria_seq', 1, false);
          public          postgres    false    219            �           0    0    cliente_id_cliente_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.cliente_id_cliente_seq', 1, false);
          public          postgres    false    221            �           0    0    conductor_id_conductor_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.conductor_id_conductor_seq', 1, false);
          public          postgres    false    241            �           0    0 &   detalle_factura_id_detalle_factura_seq    SEQUENCE SET     U   SELECT pg_catalog.setval('public.detalle_factura_id_detalle_factura_seq', 1, false);
          public          postgres    false    231            �           0    0    direccion_id_direccion_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.direccion_id_direccion_seq', 1, false);
          public          postgres    false    235            �           0    0    factura_id_factura_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.factura_id_factura_seq', 1, false);
          public          postgres    false    223            �           0    0 *   factura_proveedor_id_factura_proveedor_seq    SEQUENCE SET     Y   SELECT pg_catalog.setval('public.factura_proveedor_id_factura_proveedor_seq', 1, false);
          public          postgres    false    229            �           0    0    inventario_id_inventario_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public.inventario_id_inventario_seq', 1, false);
          public          postgres    false    225            �           0    0    orden_item_id_orden_item_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public.orden_item_id_orden_item_seq', 1, false);
          public          postgres    false    227            �           0    0    producto_id_producto_seq    SEQUENCE SET     G   SELECT pg_catalog.setval('public.producto_id_producto_seq', 1, false);
          public          postgres    false    215            �           0    0    proveedor_id_proveedor_seq    SEQUENCE SET     I   SELECT pg_catalog.setval('public.proveedor_id_proveedor_seq', 1, false);
          public          postgres    false    217            �           0    0    ruta_id_ruta_seq    SEQUENCE SET     ?   SELECT pg_catalog.setval('public.ruta_id_ruta_seq', 1, false);
          public          postgres    false    237            �           0    0    transporte_id_transporte_seq    SEQUENCE SET     K   SELECT pg_catalog.setval('public.transporte_id_transporte_seq', 1, false);
          public          postgres    false    239            �           0    0    usuario_id_usuario_seq    SEQUENCE SET     E   SELECT pg_catalog.setval('public.usuario_id_usuario_seq', 1, false);
          public          postgres    false    233            �           2606    17103    categoria categoria_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.categoria
    ADD CONSTRAINT categoria_pkey PRIMARY KEY (id_categoria);
 B   ALTER TABLE ONLY public.categoria DROP CONSTRAINT categoria_pkey;
       public            postgres    false    220            �           2606    17112    cliente cliente_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT cliente_pkey PRIMARY KEY (id_cliente);
 >   ALTER TABLE ONLY public.cliente DROP CONSTRAINT cliente_pkey;
       public            postgres    false    222            �           2606    17192    conductor conductor_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.conductor
    ADD CONSTRAINT conductor_pkey PRIMARY KEY (id_conductor);
 B   ALTER TABLE ONLY public.conductor DROP CONSTRAINT conductor_pkey;
       public            postgres    false    242            �           2606    17151 $   detalle_factura detalle_factura_pkey 
   CONSTRAINT     r   ALTER TABLE ONLY public.detalle_factura
    ADD CONSTRAINT detalle_factura_pkey PRIMARY KEY (id_detalle_factura);
 N   ALTER TABLE ONLY public.detalle_factura DROP CONSTRAINT detalle_factura_pkey;
       public            postgres    false    232            �           2606    17169    direccion direccion_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.direccion
    ADD CONSTRAINT direccion_pkey PRIMARY KEY (id_direccion);
 B   ALTER TABLE ONLY public.direccion DROP CONSTRAINT direccion_pkey;
       public            postgres    false    236            �           2606    17121    factura factura_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.factura
    ADD CONSTRAINT factura_pkey PRIMARY KEY (id_factura);
 >   ALTER TABLE ONLY public.factura DROP CONSTRAINT factura_pkey;
       public            postgres    false    224            �           2606    17144 (   factura_proveedor factura_proveedor_pkey 
   CONSTRAINT     x   ALTER TABLE ONLY public.factura_proveedor
    ADD CONSTRAINT factura_proveedor_pkey PRIMARY KEY (id_factura_proveedor);
 R   ALTER TABLE ONLY public.factura_proveedor DROP CONSTRAINT factura_proveedor_pkey;
       public            postgres    false    230            �           2606    17128    inventario inventario_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY public.inventario
    ADD CONSTRAINT inventario_pkey PRIMARY KEY (id_inventario);
 D   ALTER TABLE ONLY public.inventario DROP CONSTRAINT inventario_pkey;
       public            postgres    false    226            �           2606    17135    orden_item orden_item_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY public.orden_item
    ADD CONSTRAINT orden_item_pkey PRIMARY KEY (id_orden_item);
 D   ALTER TABLE ONLY public.orden_item DROP CONSTRAINT orden_item_pkey;
       public            postgres    false    228            �           2606    17087    producto producto_pkey 
   CONSTRAINT     ]   ALTER TABLE ONLY public.producto
    ADD CONSTRAINT producto_pkey PRIMARY KEY (id_producto);
 @   ALTER TABLE ONLY public.producto DROP CONSTRAINT producto_pkey;
       public            postgres    false    216            �           2606    17096    proveedor proveedor_pkey 
   CONSTRAINT     `   ALTER TABLE ONLY public.proveedor
    ADD CONSTRAINT proveedor_pkey PRIMARY KEY (id_proveedor);
 B   ALTER TABLE ONLY public.proveedor DROP CONSTRAINT proveedor_pkey;
       public            postgres    false    218            �           2606    17257 "   ruta_direccion ruta_direccion_pkey 
   CONSTRAINT     s   ALTER TABLE ONLY public.ruta_direccion
    ADD CONSTRAINT ruta_direccion_pkey PRIMARY KEY (id_ruta, id_direccion);
 L   ALTER TABLE ONLY public.ruta_direccion DROP CONSTRAINT ruta_direccion_pkey;
       public            postgres    false    243    243            �           2606    17176    ruta ruta_pkey 
   CONSTRAINT     Q   ALTER TABLE ONLY public.ruta
    ADD CONSTRAINT ruta_pkey PRIMARY KEY (id_ruta);
 8   ALTER TABLE ONLY public.ruta DROP CONSTRAINT ruta_pkey;
       public            postgres    false    238            �           2606    17183    transporte transporte_pkey 
   CONSTRAINT     c   ALTER TABLE ONLY public.transporte
    ADD CONSTRAINT transporte_pkey PRIMARY KEY (id_transporte);
 D   ALTER TABLE ONLY public.transporte DROP CONSTRAINT transporte_pkey;
       public            postgres    false    240            �           2606    17160    usuario usuario_pkey 
   CONSTRAINT     Z   ALTER TABLE ONLY public.usuario
    ADD CONSTRAINT usuario_pkey PRIMARY KEY (id_usuario);
 >   ALTER TABLE ONLY public.usuario DROP CONSTRAINT usuario_pkey;
       public            postgres    false    234            �           2606    17213    factura fk_cliente    FK CONSTRAINT     ~   ALTER TABLE ONLY public.factura
    ADD CONSTRAINT fk_cliente FOREIGN KEY (id_cliente) REFERENCES public.cliente(id_cliente);
 <   ALTER TABLE ONLY public.factura DROP CONSTRAINT fk_cliente;
       public          postgres    false    3533    224    222            �           2606    17278    ruta fk_conductor_ruta    FK CONSTRAINT     �   ALTER TABLE ONLY public.ruta
    ADD CONSTRAINT fk_conductor_ruta FOREIGN KEY (id_conductor) REFERENCES public.conductor(id_conductor);
 @   ALTER TABLE ONLY public.ruta DROP CONSTRAINT fk_conductor_ruta;
       public          postgres    false    3553    238    242            �           2606    17273 "   transporte fk_conductor_transporte    FK CONSTRAINT     �   ALTER TABLE ONLY public.transporte
    ADD CONSTRAINT fk_conductor_transporte FOREIGN KEY (id_conductor) REFERENCES public.conductor(id_conductor);
 L   ALTER TABLE ONLY public.transporte DROP CONSTRAINT fk_conductor_transporte;
       public          postgres    false    3553    242    240            �           2606    17208 *   detalle_factura fk_detalle_factura_factura    FK CONSTRAINT     �   ALTER TABLE ONLY public.detalle_factura
    ADD CONSTRAINT fk_detalle_factura_factura FOREIGN KEY (id_factura) REFERENCES public.factura(id_factura);
 T   ALTER TABLE ONLY public.detalle_factura DROP CONSTRAINT fk_detalle_factura_factura;
       public          postgres    false    3535    232    224            �           2606    17203 +   detalle_factura fk_detalle_factura_producto    FK CONSTRAINT     �   ALTER TABLE ONLY public.detalle_factura
    ADD CONSTRAINT fk_detalle_factura_producto FOREIGN KEY (id_producto) REFERENCES public.producto(id_producto);
 U   ALTER TABLE ONLY public.detalle_factura DROP CONSTRAINT fk_detalle_factura_producto;
       public          postgres    false    3527    232    216            �           2606    17238    proveedor fk_direccion    FK CONSTRAINT     �   ALTER TABLE ONLY public.proveedor
    ADD CONSTRAINT fk_direccion FOREIGN KEY (id_direccion) REFERENCES public.direccion(id_direccion);
 @   ALTER TABLE ONLY public.proveedor DROP CONSTRAINT fk_direccion;
       public          postgres    false    3547    218    236            �           2606    17263    ruta_direccion fk_direccion    FK CONSTRAINT     �   ALTER TABLE ONLY public.ruta_direccion
    ADD CONSTRAINT fk_direccion FOREIGN KEY (id_direccion) REFERENCES public.direccion(id_direccion);
 E   ALTER TABLE ONLY public.ruta_direccion DROP CONSTRAINT fk_direccion;
       public          postgres    false    3547    236    243            �           2606    17283    cliente fk_direccion_cliente    FK CONSTRAINT     �   ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT fk_direccion_cliente FOREIGN KEY (id_direccion) REFERENCES public.direccion(id_direccion);
 F   ALTER TABLE ONLY public.cliente DROP CONSTRAINT fk_direccion_cliente;
       public          postgres    false    3547    222    236            �           2606    17243    factura fk_direccion_factura    FK CONSTRAINT     �   ALTER TABLE ONLY public.factura
    ADD CONSTRAINT fk_direccion_factura FOREIGN KEY (id_direccion) REFERENCES public.direccion(id_direccion);
 F   ALTER TABLE ONLY public.factura DROP CONSTRAINT fk_direccion_factura;
       public          postgres    false    224    3547    236            �           2606    17228    orden_item fk_factura_proveedor    FK CONSTRAINT     �   ALTER TABLE ONLY public.orden_item
    ADD CONSTRAINT fk_factura_proveedor FOREIGN KEY (id_factura_proveedor) REFERENCES public.factura_proveedor(id_factura_proveedor);
 I   ALTER TABLE ONLY public.orden_item DROP CONSTRAINT fk_factura_proveedor;
       public          postgres    false    3541    230    228            �           2606    17198 !   inventario fk_inventario_producto    FK CONSTRAINT     �   ALTER TABLE ONLY public.inventario
    ADD CONSTRAINT fk_inventario_producto FOREIGN KEY (id_producto) REFERENCES public.producto(id_producto);
 K   ALTER TABLE ONLY public.inventario DROP CONSTRAINT fk_inventario_producto;
       public          postgres    false    226    3527    216            �           2606    17233    orden_item fk_producto    FK CONSTRAINT     �   ALTER TABLE ONLY public.orden_item
    ADD CONSTRAINT fk_producto FOREIGN KEY (id_producto) REFERENCES public.producto(id_producto);
 @   ALTER TABLE ONLY public.orden_item DROP CONSTRAINT fk_producto;
       public          postgres    false    3527    216    228            �           2606    17193    producto fk_producto_categoria    FK CONSTRAINT     �   ALTER TABLE ONLY public.producto
    ADD CONSTRAINT fk_producto_categoria FOREIGN KEY (id_categoria) REFERENCES public.categoria(id_categoria);
 H   ALTER TABLE ONLY public.producto DROP CONSTRAINT fk_producto_categoria;
       public          postgres    false    216    220    3531            �           2606    17218    factura_proveedor fk_proveedor    FK CONSTRAINT     �   ALTER TABLE ONLY public.factura_proveedor
    ADD CONSTRAINT fk_proveedor FOREIGN KEY (id_proveedor) REFERENCES public.proveedor(id_proveedor);
 H   ALTER TABLE ONLY public.factura_proveedor DROP CONSTRAINT fk_proveedor;
       public          postgres    false    218    3529    230            �           2606    17258    ruta_direccion fk_ruta    FK CONSTRAINT     y   ALTER TABLE ONLY public.ruta_direccion
    ADD CONSTRAINT fk_ruta FOREIGN KEY (id_ruta) REFERENCES public.ruta(id_ruta);
 @   ALTER TABLE ONLY public.ruta_direccion DROP CONSTRAINT fk_ruta;
       public          postgres    false    238    3549    243            �           2606    17248    factura fk_ruta_factura    FK CONSTRAINT     z   ALTER TABLE ONLY public.factura
    ADD CONSTRAINT fk_ruta_factura FOREIGN KEY (id_ruta) REFERENCES public.ruta(id_ruta);
 A   ALTER TABLE ONLY public.factura DROP CONSTRAINT fk_ruta_factura;
       public          postgres    false    238    224    3549            �           2606    17268    ruta fk_transporte_ruta    FK CONSTRAINT     �   ALTER TABLE ONLY public.ruta
    ADD CONSTRAINT fk_transporte_ruta FOREIGN KEY (id_transporte) REFERENCES public.transporte(id_transporte);
 A   ALTER TABLE ONLY public.ruta DROP CONSTRAINT fk_transporte_ruta;
       public          postgres    false    240    3551    238            �           2606    17223 $   factura_proveedor fk_usuario_factura    FK CONSTRAINT     �   ALTER TABLE ONLY public.factura_proveedor
    ADD CONSTRAINT fk_usuario_factura FOREIGN KEY (id_usuario) REFERENCES public.usuario(id_usuario);
 N   ALTER TABLE ONLY public.factura_proveedor DROP CONSTRAINT fk_usuario_factura;
       public          postgres    false    234    230    3545            �   
   x���          �   
   x���          �   
   x���          �   
   x���          �   
   x���          �   
   x���          �   
   x���          �   
   x���          �   
   x���          �   
   x���          �   
   x���          �   
   x���          �   
   x���          �   
   x���          �   
   x���         