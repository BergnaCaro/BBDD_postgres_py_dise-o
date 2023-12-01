--
-- PostgreSQL database dump
--

-- Dumped from database version 14.9
-- Dumped by pg_dump version 14.9

-- Started on 2023-08-22 15:56:58

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
-- TOC entry 214 (class 1259 OID 16467)
-- Name: cliente; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.cliente (
    codigo integer NOT NULL,
    razon_social character varying(100) NOT NULL,
    saldo_deudor numeric(10,2) DEFAULT 0 NOT NULL,
    cuit bigint NOT NULL,
    calle character varying(100) NOT NULL,
    calle_numero integer NOT NULL,
    piso integer,
    depto character(100),
    contacto character varying(100),
    nombre character varying(100) NOT NULL,
    nro integer NOT NULL,
    cp character varying(8)
);


ALTER TABLE public.cliente OWNER TO postgres;

--
-- TOC entry 219 (class 1259 OID 16534)
-- Name: compuesta; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.compuesta (
    numero integer NOT NULL,
    codigo integer NOT NULL,
    precio numeric(10,2) NOT NULL,
    cantidad integer DEFAULT 0 NOT NULL,
    subtotal numeric(10,2) GENERATED ALWAYS AS ((precio * (cantidad)::numeric)) STORED
);


ALTER TABLE public.compuesta OWNER TO postgres;

--
-- TOC entry 218 (class 1259 OID 16519)
-- Name: factura; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.factura (
    numero integer NOT NULL,
    fecha date DEFAULT CURRENT_DATE NOT NULL,
    monto_gravado numeric(10,2) NOT NULL,
    monto_no_gravado numeric(10,2) NOT NULL,
    monto_ambos numeric(10,2) GENERATED ALWAYS AS ((monto_gravado + monto_no_gravado)) STORED,
    codigo integer,
    envio boolean DEFAULT false NOT NULL,
    pagada boolean DEFAULT false NOT NULL,
    terminada boolean DEFAULT false NOT NULL,
    total_pagado numeric(10,2)
);


ALTER TABLE public.factura OWNER TO postgres;

--
-- TOC entry 213 (class 1259 OID 16462)
-- Name: localidad; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.localidad (
    codigo_postal character varying(8) NOT NULL,
    nombre character varying(100)
);


ALTER TABLE public.localidad OWNER TO postgres;

--
-- TOC entry 215 (class 1259 OID 16487)
-- Name: mayorista; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.mayorista (
    codigo integer NOT NULL,
    descuento numeric(10,2) DEFAULT 0 NOT NULL,
    CONSTRAINT ck_descuento CHECK ((descuento < 0.06))
);


ALTER TABLE public.mayorista OWNER TO postgres;

--
-- TOC entry 216 (class 1259 OID 16499)
-- Name: minorista; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.minorista (
    codigo integer NOT NULL
);


ALTER TABLE public.minorista OWNER TO postgres;

--
-- TOC entry 220 (class 1259 OID 16551)
-- Name: pago; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.pago (
    numero integer NOT NULL,
    fecha date NOT NULL,
    importe numeric(10,2) DEFAULT 0 NOT NULL
);


ALTER TABLE public.pago OWNER TO postgres;

--
-- TOC entry 209 (class 1259 OID 16425)
-- Name: producto; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.producto (
    codigo integer DEFAULT 101 NOT NULL,
    descripcion character varying(100) NOT NULL,
    stock integer DEFAULT 0 NOT NULL,
    gravado_s_n boolean,
    precio_sugerido numeric(10,2) NOT NULL,
    CONSTRAINT ck_producto_codigo CHECK ((codigo > 100))
);


ALTER TABLE public.producto OWNER TO postgres;

--
-- TOC entry 212 (class 1259 OID 16447)
-- Name: prov_zona; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.prov_zona (
    nombre character varying(100) NOT NULL,
    numero integer NOT NULL,
    costo_envio numeric(10,2)
);


ALTER TABLE public.prov_zona OWNER TO postgres;

--
-- TOC entry 210 (class 1259 OID 16433)
-- Name: provincia; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.provincia (
    nombre character varying(100) NOT NULL
);


ALTER TABLE public.provincia OWNER TO postgres;

--
-- TOC entry 217 (class 1259 OID 16509)
-- Name: telefono; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.telefono (
    numero integer NOT NULL,
    codigo integer NOT NULL
);


ALTER TABLE public.telefono OWNER TO postgres;

--
-- TOC entry 211 (class 1259 OID 16438)
-- Name: zona; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.zona (
    numero integer NOT NULL,
    CONSTRAINT ck_numero_zona CHECK (((numero > 0) AND (numero < 4)))
);


ALTER TABLE public.zona OWNER TO postgres;

--
-- TOC entry 3233 (class 2606 OID 16474)
-- Name: cliente pk_cliente; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT pk_cliente PRIMARY KEY (codigo);


--
-- TOC entry 3231 (class 2606 OID 16466)
-- Name: localidad pk_codigo_postal; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.localidad
    ADD CONSTRAINT pk_codigo_postal PRIMARY KEY (codigo_postal);


--
-- TOC entry 3243 (class 2606 OID 16528)
-- Name: factura pk_factura; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.factura
    ADD CONSTRAINT pk_factura PRIMARY KEY (numero);


--
-- TOC entry 3245 (class 2606 OID 16540)
-- Name: compuesta pk_factura_compuesta; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.compuesta
    ADD CONSTRAINT pk_factura_compuesta PRIMARY KEY (numero, codigo);


--
-- TOC entry 3237 (class 2606 OID 16493)
-- Name: mayorista pk_mayorista; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mayorista
    ADD CONSTRAINT pk_mayorista PRIMARY KEY (codigo);


--
-- TOC entry 3239 (class 2606 OID 16503)
-- Name: minorista pk_minorista; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.minorista
    ADD CONSTRAINT pk_minorista PRIMARY KEY (codigo);


--
-- TOC entry 3247 (class 2606 OID 16556)
-- Name: pago pk_pago; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pago
    ADD CONSTRAINT pk_pago PRIMARY KEY (numero, fecha);


--
-- TOC entry 3223 (class 2606 OID 16432)
-- Name: producto pk_producto_codigo; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.producto
    ADD CONSTRAINT pk_producto_codigo PRIMARY KEY (codigo);


--
-- TOC entry 3225 (class 2606 OID 16437)
-- Name: provincia pk_provincia; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.provincia
    ADD CONSTRAINT pk_provincia PRIMARY KEY (nombre);


--
-- TOC entry 3241 (class 2606 OID 16513)
-- Name: telefono pk_telefono; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.telefono
    ADD CONSTRAINT pk_telefono PRIMARY KEY (numero);


--
-- TOC entry 3227 (class 2606 OID 16443)
-- Name: zona pk_zona; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.zona
    ADD CONSTRAINT pk_zona PRIMARY KEY (numero);


--
-- TOC entry 3229 (class 2606 OID 16451)
-- Name: prov_zona pk_zona2; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prov_zona
    ADD CONSTRAINT pk_zona2 PRIMARY KEY (nombre, numero);


--
-- TOC entry 3235 (class 2606 OID 16476)
-- Name: cliente uk_cliente; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT uk_cliente UNIQUE (cuit);


--
-- TOC entry 3251 (class 2606 OID 16482)
-- Name: cliente fk_cliente_loc; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT fk_cliente_loc FOREIGN KEY (cp) REFERENCES public.localidad(codigo_postal);


--
-- TOC entry 3252 (class 2606 OID 16494)
-- Name: mayorista fk_cliente_mayorista; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.mayorista
    ADD CONSTRAINT fk_cliente_mayorista FOREIGN KEY (codigo) REFERENCES public.cliente(codigo);


--
-- TOC entry 3253 (class 2606 OID 16504)
-- Name: minorista fk_cliente_minorista; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.minorista
    ADD CONSTRAINT fk_cliente_minorista FOREIGN KEY (codigo) REFERENCES public.cliente(codigo);


--
-- TOC entry 3250 (class 2606 OID 16477)
-- Name: cliente fk_cliente_prov_zona; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.cliente
    ADD CONSTRAINT fk_cliente_prov_zona FOREIGN KEY (nombre, nro) REFERENCES public.prov_zona(nombre, numero);


--
-- TOC entry 3255 (class 2606 OID 16529)
-- Name: factura fk_factura_cliente; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.factura
    ADD CONSTRAINT fk_factura_cliente FOREIGN KEY (codigo) REFERENCES public.cliente(codigo);


--
-- TOC entry 3256 (class 2606 OID 16541)
-- Name: compuesta fk_factura_compuesta; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.compuesta
    ADD CONSTRAINT fk_factura_compuesta FOREIGN KEY (numero) REFERENCES public.factura(numero);


--
-- TOC entry 3258 (class 2606 OID 16557)
-- Name: pago fk_pago_factura; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.pago
    ADD CONSTRAINT fk_pago_factura FOREIGN KEY (numero) REFERENCES public.factura(numero);


--
-- TOC entry 3257 (class 2606 OID 16546)
-- Name: compuesta fk_producto_factura; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.compuesta
    ADD CONSTRAINT fk_producto_factura FOREIGN KEY (codigo) REFERENCES public.producto(codigo);


--
-- TOC entry 3248 (class 2606 OID 16452)
-- Name: prov_zona fk_prov_zona_provincia; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prov_zona
    ADD CONSTRAINT fk_prov_zona_provincia FOREIGN KEY (nombre) REFERENCES public.provincia(nombre);


--
-- TOC entry 3249 (class 2606 OID 16457)
-- Name: prov_zona fk_prov_zona_zona; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.prov_zona
    ADD CONSTRAINT fk_prov_zona_zona FOREIGN KEY (numero) REFERENCES public.zona(numero);


--
-- TOC entry 3254 (class 2606 OID 16514)
-- Name: telefono fk_telefono_cliente; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.telefono
    ADD CONSTRAINT fk_telefono_cliente FOREIGN KEY (codigo) REFERENCES public.cliente(codigo);


-- Completed on 2023-08-22 15:56:58

--
-- PostgreSQL database dump complete
--

