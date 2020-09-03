--
-- PostgreSQL database dump
--

-- Dumped from database version 12.4
-- Dumped by pg_dump version 12.4

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: hadi
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO hadi;

--
-- Name: books; Type: TABLE; Schema: public; Owner: hadi
--

CREATE TABLE public.books (
    id integer NOT NULL,
    name character varying NOT NULL,
    category_id integer NOT NULL
);


ALTER TABLE public.books OWNER TO hadi;

--
-- Name: books_id_seq; Type: SEQUENCE; Schema: public; Owner: hadi
--

CREATE SEQUENCE public.books_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.books_id_seq OWNER TO hadi;

--
-- Name: books_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hadi
--

ALTER SEQUENCE public.books_id_seq OWNED BY public.books.id;


--
-- Name: categories; Type: TABLE; Schema: public; Owner: hadi
--

CREATE TABLE public.categories (
    id integer NOT NULL,
    name character varying NOT NULL
);


ALTER TABLE public.categories OWNER TO hadi;

--
-- Name: categories_id_seq; Type: SEQUENCE; Schema: public; Owner: hadi
--

CREATE SEQUENCE public.categories_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.categories_id_seq OWNER TO hadi;

--
-- Name: categories_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: hadi
--

ALTER SEQUENCE public.categories_id_seq OWNED BY public.categories.id;


--
-- Name: books id; Type: DEFAULT; Schema: public; Owner: hadi
--

ALTER TABLE ONLY public.books ALTER COLUMN id SET DEFAULT nextval('public.books_id_seq'::regclass);


--
-- Name: categories id; Type: DEFAULT; Schema: public; Owner: hadi
--

ALTER TABLE ONLY public.categories ALTER COLUMN id SET DEFAULT nextval('public.categories_id_seq'::regclass);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: hadi
--

COPY public.alembic_version (version_num) FROM stdin;
e1a757fd0ee5
\.


--
-- Data for Name: books; Type: TABLE DATA; Schema: public; Owner: hadi
--

COPY public.books (id, name, category_id) FROM stdin;
22	Nizar Qabani Poems	3
23	update book	4
\.


--
-- Data for Name: categories; Type: TABLE DATA; Schema: public; Owner: hadi
--

COPY public.categories (id, name) FROM stdin;
2	Islamic
3	History
4	Poem
5	Poem
6	Poems
\.


--
-- Name: books_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hadi
--

SELECT pg_catalog.setval('public.books_id_seq', 24, true);


--
-- Name: categories_id_seq; Type: SEQUENCE SET; Schema: public; Owner: hadi
--

SELECT pg_catalog.setval('public.categories_id_seq', 6, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: hadi
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: books books_pkey; Type: CONSTRAINT; Schema: public; Owner: hadi
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_pkey PRIMARY KEY (id);


--
-- Name: categories categories_pkey; Type: CONSTRAINT; Schema: public; Owner: hadi
--

ALTER TABLE ONLY public.categories
    ADD CONSTRAINT categories_pkey PRIMARY KEY (id);


--
-- Name: books books_category_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: hadi
--

ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_category_id_fkey FOREIGN KEY (category_id) REFERENCES public.categories(id);


--
-- PostgreSQL database dump complete
--

